"""Contains implementation for evoked info"""

from meggie.mainwindow.dynamic import InfoAction


class Info(InfoAction):
    """Fills up evoked info box"""

    def run(self, params={}):
        try:
            selected_name = self.data["outputs"]["evoked"][0]
            evoked = self.experiment.active_subject.evoked[selected_name]
            params = evoked.params

            message = ""

            message += "Name: {}\n\n".format(evoked.name)

            if "conditions" in params:
                message += "Conditions: " + ", ".join(params["conditions"]) + "\n"

            if "groups" in params:
                for key, names in params["groups"].items():
                    message += "\nGroup " + str(key) + ": \n"
                    for name in names:
                        message += name + "\n"

        except Exception:
            message = ""

        return message
