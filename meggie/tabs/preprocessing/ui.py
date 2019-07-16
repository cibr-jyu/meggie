"""
"""

def plot(subject, data):
    raw = subject.get_working_file()
    if raw:
        raw.plot()
    

