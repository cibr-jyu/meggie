
# coding: utf-8
"""
"""

import logging

import mne

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

from meggie.utilities.decorators import threaded


def prepare_data_for_permutation(experiment, design, groups, conditions,
                                 item_type, item_name, 
                                 location_limits, time_limits, frequency_limits,
                                 data_format=('locations', 'freqs', 'times')):
    """
    """
    final_data = {}
    if design == 'between-subjects':
        for condition in conditions:
            cond_data = []
            for group in groups.values():
                group_data = []
                for subject_name in group:
                    subject = experiment.subjects[subject_name]
                    subject_item = getattr(subject, item_type).get(item_name)
                    if not subject_item:
                        message = "Skipping " + subject_name + " (no " + str(item_type) + ")"
                        logging.getLogger('ui_logger').warning(message) 

                    data = subject_item.data[condition]
                    if frequency_limits is not None:
                        # average over the selected frequency range
                        freqs = subject_item.freqs
                        fmin_idx = np.where(freqs >= frequency_limits[0])[0][0]
                        fmax_idx = np.where(freqs <= frequency_limits[1])[0][-1]
                        swapped = np.swapaxes(data, data_format.index('freqs'), 0)
                        averaged = np.mean(swapped[fmin_idx:fmax_idx], axis=0)[np.newaxis, :]
                        data = np.swapaxes(averaged, data_format.index('freqs'), 0)
                    if location_limits is not None:
                        # take the seleted location
                        ch_names = subject_item.ch_names
                        ch_idx = ch_names.index(location_limits)
                        swapped = np.swapaxes(data, data_format.index('locations'), 0)
                        selected = data[ch_idx][np.newaxis, :]
                        data = np.swapaxes(selected, data_format.index('locations'), 0)
                    if time_limits is not None:
                        # average over the selected temporal range
                        times = subject_item.times
                        tmin_idx = np.where(times >= time_limits[0])[0][0]
                        tmax_idx = np.where(times <= time_limits[1])[0][-1]
                        swapped = np.swapaxes(data, data_format.index('times'), 0)
                        averaged = np.mean(swapped[tmin_idx:tmax_idx], axis=0)[np.newaxis, :]
                        data = np.swapaxes(averaged, data_format.index('times'), 0)

                    # move locations dim to last place
                    data = np.rollaxis(data, data_format.index('locations'), data.ndim)

                    group_data.append(data)
                cond_data.append(np.array(group_data))
            final_data[condition] = cond_data
        return final_data
    elif design == 'within-subjects':
        final_data = {}
        for group_key, group in groups.items():

            group_data = []
            for subject_idx, subject_name in enumerate(group):
                subject = experiment.subjects[subject_name]
                subject_item = getattr(subject, item_type).get(item_name)
                if not subject_item:
                    message = "Skipping " + subject_name + " (no " + str(item_type) + ")"
                    logging.getLogger('ui_logger').warning(message) 

                cond_data = []
                for condition_idx, condition in enumerate(conditions):
                    data = subject_item.data[condition]
                    if frequency_limits is not None:
                        # average over the selected frequency range
                        freqs = subject_item.freqs
                        fmin_idx = np.where(freqs >= frequency_limits[0])[0][0]
                        fmax_idx = np.where(freqs <= frequency_limits[1])[0][-1]
                        swapped = np.swapaxes(data, data_format.index('freqs'), 0)
                        averaged = np.mean(swapped[fmin_idx:fmax_idx], axis=0)[np.newaxis, :]
                        data = np.swapaxes(averaged, data_format.index('freqs'), 0)
                    if location_limits is not None:
                        # take the seleted location
                        ch_names = subject_item.ch_names
                        ch_idx = ch_names.index(location_limits)
                        swapped = np.swapaxes(data, data_format.index('locations'), 0)
                        selected = data[ch_idx][np.newaxis, :]
                        data = np.swapaxes(selected, data_format.index('locations'), 0)
                    if time_limits is not None:
                        # average over the selected temporal range
                        times = subject_item.times
                        tmin_idx = np.where(times >= time_limits[0])[0][0]
                        tmax_idx = np.where(times <= time_limits[1])[0][-1]
                        swapped = np.swapaxes(data, data_format.index('times'), 0)
                        averaged = np.mean(swapped[tmin_idx:tmax_idx], axis=0)[np.newaxis, :]
                        data = np.swapaxes(averaged, data_format.index('times'), 0)
                    cond_data.append(data)
                group_data.append(cond_data)

            # The format needed is:
            # (n_conds, n_subjects, ..., n_channels)
            swapped = np.swapaxes(np.array(group_data), 0, 1)
            rolled = np.rollaxis(swapped, 2 + data_format.index('locations'), swapped.ndim)
            final_data[group_key] = rolled
            return final_data
    else:
        raise Exception("Only within and between subjects designs are supported")


@threaded
def permutation_analysis(data, design, conditions, groups, threshold, adjacency, n_permutations):
    results = {}
    if design == 'between-subjects':
        for condition in conditions:
            X = data[condition]

            # Have to implement F-from-p computation here.
            num_df = len(groups.keys()) - 1
            denom_df = sum([len(lst) for lst in groups.values()]) - len(groups.keys())
            crit_val = scipy.stats.f.ppf(q=1-threshold, dfn=num_df, dfd=denom_df)

            res = mne.stats.permutation_cluster_test(
                X=X,
                threshold=threshold,
                n_permutations=n_permutations,
                adjacency=adjacency,
                verbose='warning',
                out_type='indices'
            )
            results[condition] = res
    else:
        for group_key, group in groups.items():
            X = data[group_key]
            factor_levels, effects = [2], 'A'
            f_thresh = mne.stats.f_threshold_mway_rm(len(group), factor_levels, effects, threshold)

            def stat_fun(*args):
                return mne.stats.f_mway_rm(np.swapaxes(args, 1, 0), factor_levels=factor_levels,
                                           effects=effects, return_pvals=False)[0]

            res = mne.stats.permutation_cluster_test(
                X=X,
                adjacency=adjacency,
                threshold=f_thresh,
                stat_fun=stat_fun,
                n_permutations=n_permutations,
                verbose='warning',
                out_type='indices'
            )
            results[group_key] = res
        return results


def report_permutation_results(results, selected_name, significance, location_limits=None, frequency_limits=None, time_limits=None):
    """
    """
    logger = logging.getLogger('ui_logger')
    logger.info('Permutation tests for ' + str(selected_name) + ' completed.')
    if location_limits:
        logger.info('Location limits: ' + str(location_limits))
    if frequency_limits:
        logger.info('Frequency limits: ' + str(frequency_limits))
    if time_limits:
        logger.info('Time limits: ' + str(time_limits))

    for key, res in results.items():
        n_clusters = len(res[2])
        sign_mask = np.where(res[2] < significance)[0]
        n_sign_clusters = len(sign_mask)

        logger.info('Found ' + str(n_clusters) +
                    ' clusters (' + str(n_sign_clusters) +
                    ' significant) for ' + str(key))

    
def plot_permutation_results(results, significance, 
                             location_limits=None, frequency_limits=None, time_limits=None,
                             frequency_fun=None, time_fun=None, location_fun=None):
    """
    """
    for key, res in results.items():
        sign_mask = np.where(res[2] < significance)[0]
        n_sign_clusters = len(sign_mask)
        for sign_idx in range(n_sign_clusters):
            cluster = res[1][sign_mask[sign_idx]]
            pvalue = res[2][sign_mask[sign_idx]]
            if frequency_limits is None:
                fig, ax = plt.subplots()
                fig.suptitle(str(key) + ': cluster ' + str(sign_idx+1) + ' (p ' + str(pvalue) + ')')
                if frequency_fun:
                    frequency_fun(cluster, ax, key)
            if location_limits is None:
                # spectrum object does not contain locations but may have less channels
                # so filter the info to contain only channels that the spectrum object has
                fig, ax = plt.subplots()
                fig.suptitle(str(key) + ': cluster ' + str(sign_idx+1) + ' (p ' + str(pvalue) + ')')
                if location_fun:
                    location_fun(cluster, ax, key)
            plt.show()

