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


if __name__ == '__main__':
    names = ["kissa", "koira", "kissa_1", "kissa_2", "kissa_11"]
    assert(next_available_name(names, "kissa") == 'kissa_12')
    assert(next_available_name(names, "koira") == 'koira_1')
    assert(next_available_name(names, "kettu") == 'kettu')

