from meggie.utilities.plotting import color_cycle

def test_color_cycle():
    colors = color_cycle(30)
    assert(type(colors) == list)
    assert(len(colors) == 30)
    assert(len(set(colors)) == 8)

