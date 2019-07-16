"""
"""


def plot(subject, data):
    raw = subject.get_working_file()
    if raw:
        raw.plot()


def projections(subject, data):
    raw = subject.get_working_file()
    if not raw.info['projs']:
        messagebox(self, "No added projections.")
        return

    fig = raw.plot_projs_topomap()

    name = subject.subject_name 
    fig.canvas.set_window_title('Projections for ' + name)

