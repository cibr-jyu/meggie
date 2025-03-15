import io
import re
import os
import sys
import pytest
import joblib
import meggie.utilities.threading
from pprint import pprint
from contextlib import redirect_stdout


def patched_progress(self):
    return


joblib.parallel.Parallel.print_progress = patched_progress


def patched_threaded(func):
    def decorated(*args, **kwargs):
        kwargs.pop("do_meanwhile", None)
        return func(*args, **kwargs)

    return decorated


meggie.utilities.threading.threaded = patched_threaded


class TraceCallInfo:
    idx = 0
    all_calls = []
    good_calls = []


def trace_calls(frame, event, arg):

    if event != "call":
        return trace_calls

    co = frame.f_code
    func_name = co.co_name
    file_name = os.path.abspath(co.co_filename)

    caller = frame.f_back
    if not caller:
        return trace_calls

    caller_co = caller.f_code
    caller_func_name = caller_co.co_name
    caller_file_name = os.path.abspath(caller_co.co_filename)

    TraceCallInfo.idx += 1
    TraceCallInfo.all_calls.append(
        f"{file_name}:{co.co_firstlineno} {func_name} from {caller_file_name}:{caller.f_lineno} {caller_func_name}"
    )

    if "_bootstrap" in caller_file_name:
        return trace_calls

    if "<string>" in caller_file_name:
        return trace_calls

    if "testing.py" in caller_file_name:
        return trace_calls

    if "decorator-gen" in caller_file_name:
        return trace_calls

    if "listcomp" in caller_func_name:
        return trace_calls

    if "decorator-gen" in file_name and "meggie/" in caller_file_name:

        try:
            with open(caller_file_name, "r") as f:
                lines = f.readlines()
                caller_line = lines[caller.f_lineno - 1]
        except:
            caller_line = ""
        TraceCallInfo.good_calls.append((TraceCallInfo.idx, caller_line))
        return trace_calls

    if "meggie/" not in caller_file_name or "mne/" not in file_name:
        return trace_calls

    try:
        with open(caller_file_name, "r") as f:
            lines = f.readlines()
            caller_line = lines[caller.f_lineno - 1]
    except:
        caller_line = ""
    TraceCallInfo.good_calls.append((TraceCallInfo.idx, caller_line))

    return trace_calls


class TracePlugin:
    def pytest_configure(self, config):
        # When pytest starts, set up the tracing
        sys.settrace(trace_calls)

    def pytest_unconfigure(self, config):
        # When pytest finishes, tear down the tracing
        sys.settrace(None)


def mne_functions_by_actions():

    action_contents = os.listdir("meggie/actions")
    actions = []
    for name in action_contents:
        if os.path.isfile(f"meggie/actions/{name}/configuration.json"):
            actions.append(name)

    functions_by_actions = {}

    for action in actions:

        functions = []

        action_tests = os.listdir(f"meggie/actions/{action}/tests")
        for test_fname in action_tests:

            test_path = f"meggie/actions/{action}/tests/{test_fname}"

            if not os.path.isfile(test_path) or not test_fname.startswith("test_"):
                continue

            print(f"Tracing mne function calls for action test {test_path}:")

            TraceCallInfo.idx = 0
            TraceCallInfo.all_calls = []
            TraceCallInfo.good_calls = []

            stdout_capture = io.StringIO()
            with redirect_stdout(stdout_capture):
                ret_val = pytest.main(
                    ["--capture=no", test_path], plugins=[TracePlugin()]
                )
            output = stdout_capture.getvalue()
            stdout_capture.close()

            run_action_idxs = [
                idx
                for (idx, line) in enumerate(TraceCallInfo.all_calls)
                if "run_action" in line
            ]
            if not run_action_idxs:
                continue

            relevant_lines = [
                line
                for (idx, line) in TraceCallInfo.good_calls
                if idx >= run_action_idxs[0]
            ]

            results = extract_function_calls(relevant_lines)

            fuzzy_blacklist = [
                "copy",
                "list",
                "append",
                "set",
                "enumerate",
                "sorted",
                "len",
                "format",
                "join",
                "values",
                "crop",
                "floor",
                "flatten",
                "mean",
            ]
            exact_blacklist = [
                "pick",
                "drop_channels",
                "channel_type",
                "_prepare_raw_for_changes",
                "plot_changes",
                "func",
                "sources.plot",
                "dialog.add_intervals",
            ]

            def map_line(line, action):
                action_stem = action.split("_")[0]
                if "self._content" in line:
                    line = line.replace("self._content", action_stem)
                if "self.content" in line:
                    line = line.replace("self.content", action_stem)
                if "self.ica" in line:
                    line = line.replace("self.ica", "ica")
                if "self._raw" in line:
                    line = line.replace("self._raw", "raw")
                if "mne_epochs" in line:
                    line = line.replace("mne_epochs", "epochs")
                if "mne_evoked" in line:
                    line = line.replace("mne_evoked", "evoked")
                if "mne_tfr" in line:
                    line = line.replace("mne_tfr", "tfr")

                line = line.replace("raw_from", "raw")
                line = line.replace("raw_to", "raw")
                line = line.replace("raw_block", "raw")

                return line

            filtered = []
            for result in results:
                if any([item in result for item in fuzzy_blacklist]):
                    continue

                if any([item == result for item in exact_blacklist]):
                    continue

                filtered.append(map_line(result, action))

            functions.extend(filtered)
            print(filtered)

        functions_by_actions[action] = list(set(functions))

    return functions_by_actions


def remove_string_literals(line):
    pattern = r"(\'(?:\\.|[^\\\'])*\'|\"(?:\\.|[^\\\"])*\")"
    return re.sub(pattern, "", line)


def find_potential_calls(cleaned_line):
    pattern = r"\b[\w\.]+(?=\()"
    return re.findall(pattern, cleaned_line)


def clean_and_validate_call(call):
    parts = call.split(".")
    valid_parts = []
    for part in parts:
        if re.match(r"^\w[\w\d_]*$", part):
            valid_parts.append(part)
    valid_call = ".".join(valid_parts)
    return valid_call if valid_call else None


def extract_function_calls(lines):
    extracted_calls = set()

    for line in lines:
        cleaned_line = remove_string_literals(line)
        potential_calls = find_potential_calls(cleaned_line)

        for call in potential_calls:
            valid_call = clean_and_validate_call(call)
            if valid_call:
                extracted_calls.add(valid_call)

    return sorted(list(extracted_calls))


if __name__ == "__main__":

    functions_by_actions = mne_functions_by_actions()
    pprint(functions_by_actions)
