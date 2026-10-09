from unittest.mock import Mock
from urllib.parse import urlparse

import pytest
from requests import Response
from requests.exceptions import HTTPError

from meggie.utilities.datasets import get_open_datasets
from meggie.mainwindow.preferences import PreferencesHandler


@pytest.mark.parametrize("dataset_key", get_open_datasets())
def test_create_open_datasets(dataset_key, tmp_path):
    prefs = PreferencesHandler()
    prefs.workspace = str(tmp_path)

    dataset = get_open_datasets()[dataset_key]
    try:
        dataset["constructor"](
            dataset["title"], "", prefs, set_previous_experiment=False
        )
    except HTTPError as error:
        response = error.response
        if response is not None and response.status_code == 429:
            host = urlparse(response.url).hostname or ""
            if host == "osf.io" or host.endswith(".osf.io"):
                pytest.skip(f"{dataset_key}: OSF download throttled (HTTP 429)")
        raise


@pytest.fixture
def open_dataset_constructor(monkeypatch):
    constructor = Mock()
    monkeypatch.setattr(
        f"{__name__}.get_open_datasets",
        lambda: {"limo": {"title": "MNE LIMO Dataset", "constructor": constructor}},
    )
    return constructor


def test_open_dataset_constructor_success(open_dataset_constructor, tmp_path):
    test_create_open_datasets("limo", tmp_path)

    open_dataset_constructor.assert_called_once()
    args, kwargs = open_dataset_constructor.call_args
    assert args[:2] == ("MNE LIMO Dataset", "")
    assert isinstance(args[2], PreferencesHandler)
    assert args[2].workspace == str(tmp_path)
    assert kwargs == {"set_previous_experiment": False}


@pytest.mark.parametrize(
    "host", ["osf.io", "api.osf.io", "files.osf.io", "files.de-1.osf.io"]
)
def test_open_dataset_osf_throttling(open_dataset_constructor, tmp_path, host):
    response = Response()
    response.status_code = 429
    response.url = f"https://{host}/download"
    open_dataset_constructor.side_effect = HTTPError(response=response)

    with pytest.raises(pytest.skip.Exception, match="limo:.*OSF.*HTTP 429"):
        test_create_open_datasets("limo", tmp_path)


@pytest.mark.parametrize(
    "status, url",
    [
        (403, "https://files.de-1.osf.io/download"),
        (404, "https://files.de-1.osf.io/download"),
        (500, "https://files.de-1.osf.io/download"),
        (429, "https://example.com/download"),
        (429, "https://osf.io.example.com/download"),
        (429, "https://notosf.io/download"),
        (429, ""),
    ],
)
def test_open_dataset_http_error_propagates(
    open_dataset_constructor, tmp_path, status, url
):
    response = Response()
    response.status_code = status
    response.url = url
    error = HTTPError(response=response)
    open_dataset_constructor.side_effect = error

    with pytest.raises(HTTPError) as caught:
        test_create_open_datasets("limo", tmp_path)
    assert caught.value is error


@pytest.mark.parametrize("error", [HTTPError("no response"), RuntimeError("failed")])
def test_open_dataset_other_error_propagates(open_dataset_constructor, tmp_path, error):
    open_dataset_constructor.side_effect = error

    with pytest.raises(type(error)) as caught:
        test_create_open_datasets("limo", tmp_path)
    assert caught.value is error
