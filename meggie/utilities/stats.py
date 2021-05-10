
# coding: utf-8
"""
"""

import logging

from collections import OrderedDict

import mne

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import scipy


from meggie.utilities.decorators import threaded
from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.channels import pairless_grads
from meggie.utilities.channels import clean_names
from meggie.utilities.messaging import questionbox


@threaded
def prepare_data_for_permutation(experiment, design, groups,
                                 item_type, item_name, 
                                 location_limits, time_limits, frequency_limits,
                                 data_format=('locations', 'freqs', 'times')):
    """
    """
    logging.getLogger('ui_logger').info('Preparing data for permutations..')
    meggie_item = getattr(experiment.active_subject, item_type)[item_name]
    conditions = list(meggie_item.content.keys())
    groups = OrderedDict(sorted(groups.items()))

    if location_limits[0] == 'ch_type':
        # find channels shared by all subjects
        ch_names = []
        for group_key, group_subjects in groups.items():
            for subject_name in group_subjects:
                subject = experiment.subjects.get(subject_name)
                meggie_item = getattr(subject, item_type).get(item_name)
                if meggie_item:
                    ch_names.append(tuple(meggie_item.ch_names))
        common_ch_names = list(set.intersection(*map(set, ch_names)))

        # filter to selected channel type
        ch_type = location_limits[1]
        chs_by_type = get_channels_by_type(meggie_item.info)
        common_ch_names = [ch_name for ch_name in common_ch_names
                           if ch_name in chs_by_type[ch_type]]

        # remove pairless grads
        if ch_type == 'grad':
            pairless_idxs = pairless_grads(common_ch_names)
            common_ch_names = [ch_name for ch_idx, ch_name in enumerate(common_ch_names)
                               if ch_idx not in pairless_idxs]

        # update info to match valid channels
        info_ch_names = meggie_item.info['ch_names']
        picks = [ch_idx for ch_idx, ch_name in enumerate(info_ch_names)
                 if ch_name in common_ch_names]
        info = mne.pick_info(meggie_item.info.copy(), sel=picks) 

        # find adjacency matching adjacency
        adjacency, adjacency_ch_names = mne.channels.find_ch_adjacency(info, ch_type)
        cleaned_common = clean_names(common_ch_names)
        kept_idxs = [idx for idx in range(adjacency.shape[0]) if
                     adjacency_ch_names[idx] in cleaned_common]

        adjacency_arr = adjacency.toarray()[kept_idxs][:, kept_idxs]
        adjacency = scipy.sparse.csr_matrix(adjacency_arr)
    else:
        adjacency = scipy.sparse.csr_matrix([1])
        info = meggie_item.info

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
                    if location_limits[0] == 'ch_name':
                        # take the seleted location
                        ch_names = subject_item.ch_names
                        ch_idx = ch_names.index(location_limits[1])
                        swapped = np.swapaxes(data, data_format.index('locations'), 0)
                        selected = data[ch_idx][np.newaxis, :]
                        data = np.swapaxes(selected, data_format.index('locations'), 0)
                    elif location_limits[0] == 'ch_type':
                        # filter to channel type
                        ch_idxs = np.array([ch_idx for ch_idx, ch_name in enumerate(subject_item.info['ch_names'])
                                            if ch_name in common_ch_names])
                        swapped = np.swapaxes(data, data_format.index('locations'), 0)
                        selected = data[ch_idxs]
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
    elif design == 'within-subjects':
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
                    if location_limits[0] == 'ch_name':
                        # take the seleted location
                        ch_names = subject_item.ch_names
                        ch_idx = ch_names.index(location_limits[1])
                        swapped = np.swapaxes(data, data_format.index('locations'), 0)
                        selected = data[ch_idx][np.newaxis, :]
                        data = np.swapaxes(selected, data_format.index('locations'), 0)
                    elif location_limits[0] == 'ch_type':
                        # filter to channel type
                        ch_idxs = np.array([ch_idx for ch_idx, ch_name in enumerate(subject_item.ch_names)
                                            if ch_name in common_ch_names])
                        swapped = np.swapaxes(data, data_format.index('locations'), 0)
                        selected = data[ch_idxs]
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
    return info, final_data, adjacency


@threaded
def permutation_analysis(data, design, conditions, groups, threshold, adjacency, n_permutations, 
                         random_state=None):

    # if 3d (or higher) clusters, create combined for adjacency
    # as mne flattens all but the first dimension
    sample_shape = list(data.values())[0][0][0].shape
    if len(sample_shape) > 2:
        combined_adjacency = mne.stats.combine_adjacency(
            *sample_shape[1:-1], adjacency)
    else:
        combined_adjacency = adjacency

    logging.getLogger('ui_logger').info('Running permutation tests..')
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
                adjacency=combined_adjacency,
                verbose='warning',
                out_type='indices',
                seed=random_state
            )
            results[condition] = res
    else:
        for group_key, group in groups.items():
            X = data[group_key]
            factor_levels, effects = [2], 'A'
            f_thresh = mne.stats.f_threshold_mway_rm(len(group), factor_levels, effects, threshold)

            # data before: (n_conditions, n_subjects, ..., n_locations)
            # give to permutation_cluster test as: (n_conditions * n_subjects, ..., n_locations)
            # and format again properly at stat_fun for f_mway_rm: (n_subjects, n_conditions, n_others)
            # np.allclose(np.array(np.split(np.concatenate(X, axis=0), X.shape[0])), X) == True

            n_conditions = X.shape[0]
            def stat_fun(*args):
                sample = args[0]
                formatted = np.swapaxes(np.array(np.split(sample, n_conditions)), 0, 1)
                return mne.stats.f_mway_rm(formatted, factor_levels=factor_levels,
                                           effects=effects, return_pvals=False)[0]

            res = mne.stats.permutation_cluster_test(
                X=[np.concatenate(X, axis=0)],
                adjacency=combined_adjacency,
                threshold=f_thresh,
                stat_fun=stat_fun,
                n_permutations=n_permutations,
                verbose='warning',
                out_type='indices',
                seed=random_state
            )
            results[group_key] = res
    return results


def report_permutation_results(results, design, selected_name, significance, location_limits=None, frequency_limits=None, time_limits=None):
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

        if design == 'within-subjects':
            message = 'Found {0} clusters ({1} significant) for group {2}.'
        else:
            message = 'Found {0} clusters ({1} significant) for condition {2}.'
        logger.info(message.format(n_clusters, n_sign_clusters, key))

        for cluster_idx in range(n_sign_clusters):
            pvalue = res[2][sign_mask][cluster_idx]
            message = 'Cluster {0} has p value: {1}.'
            logger.info(message.format(cluster_idx + 1, pvalue))


    
def plot_permutation_results(results, significance, window,
                             location_limits=None, frequency_limits=None, time_limits=None,
                             frequency_fun=None, time_fun=None, location_fun=None):
    """
    """
    for key, res in results.items():
        sign_mask = np.where(res[2] < significance)[0]
        n_sign_clusters = len(sign_mask)

        def plot():
            for sign_idx in range(n_sign_clusters):
                cluster = res[1][sign_mask[sign_idx]]
                pvalue = res[2][sign_mask[sign_idx]]
                if frequency_limits is None:
                    if frequency_fun:
                        frequency_fun(sign_idx, cluster, pvalue, key)
                if time_limits is None:
                    if time_fun:
                        time_fun(sign_idx, cluster, pvalue, key)
                if location_limits is None or location_limits[0] == 'ch_type':
                    if location_fun:
                        location_fun(sign_idx, cluster, pvalue, key)
                plt.show()

        if n_sign_clusters > 10:
            def handler(accepted):
                if accepted:
                    plot()
            message = (str(n_sign_clusters) + ' significant clusters were found for ' +
                       str(key) + '. Do you want to plot all of them?')
            questionbox(window, message, handler)
        else:
            plot()

