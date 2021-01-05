import re


def next_available_name(old_names, stem):
    """ Given list of existing names (such as cat_1, cat_2) 
    and a stem (cat), find next name in order (cat_3)
    """
    suffices = []
    for old_name in old_names:
        template = stem + r'([_]?)' + r'([0-9]*)$'
        match = re.match(template, old_name)
        if match:
            suffix = match.group(2)
            if suffix == '':
                suffix = 0
            suffices.append(int(suffix))

    if not suffices:
        return stem

    return stem + '_' + str(max(suffices)+1)

