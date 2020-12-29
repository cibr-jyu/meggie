import re


def next_available_name(old_names, stem):
    """ 
    """
    suffices = []
    for old_name in old_names:
        template = stem + r'([_]?)' + r'([0-9]*)'
        match = re.match(template, old_name)
        if match:
            suffix = match.group(2)
            if suffix == '':
                suffix = 0
            suffices.append(int(suffix))

    if not suffices:
        return stem

    return stem + '_' + str(max(suffices)+1)

