import json

import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _list, _status_true, _test_suite

from qaseio.client.models import (
    TestSuiteCreate,
    TestSuiteCreated,
    TestSuiteFilters,
    TestSuiteInfo,
    TestSuiteList,
    TestSuiteUpdate,
)


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30), "?limit=10&offset=30"),
        ((None, 30), "?offset=30"),
        ((10, None), "?limit=10"),
        (
            (
                10,
                None,
                TestSuiteFilters(search="123"),
            ),
            "?limit=10&filters%5Bsearch%5D=123",
        ),
    ],
)
def test_get_all_test_suites(client, params, query):
    response = _status_true(_list(_test_suite()))
    with requests_mock.Mocker() as m:
        m.get(client._path("suite/CODE"), json=response)
        data = client.suites.get_all("CODE", *params)
        assert data == converter.structure(
            response.get("result"), TestSuiteList
        )
        res = client.suites._last_res
        assert res.url == client._path("suite/CODE" + query)


def test_get_specific_test_suite(client):
    response = _status_true(_test_suite())
    with requests_mock.Mocker() as m:
        m.get(client._path("suite/CODE/123"), json=response)
        data = client.suites.get("CODE", 123)
        assert data == converter.structure(
            response.get("result"), TestSuiteInfo
        )
        res = client.suites._last_res
        assert res.url == client._path("suite/CODE/123")


def test_test_suite_exists(client):
    response = _status_true(_test_suite())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("suite/CODE/123"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.suites.exists("CODE", 123)
        assert not client.suites.exists("CODE", 123)


def test_create_new_test_suite(client):
    response = _status_true({"id": 123})
    with requests_mock.Mocker() as m:
        m.post(client._path("suite/CODE"), json=response)
        create_data = TestSuiteCreate("new test suite")
        data = client.suites.create("CODE", create_data)
        assert data == converter.structure(
            response.get("result"), TestSuiteCreated
        )
        res = client.suites._last_res
        assert json.loads(res.request.body) == converter.unstructure(
            create_data
        )


def test_update_test_suite(client):
    response = _status_true({"id": 123})
    with requests_mock.Mocker() as m:
        m.patch(client._path("suite/CODE/123"), json=response)
        update_data = TestSuiteUpdate("new test plan")
        data = client.suites.update("CODE", 123, update_data)
        assert data == converter.structure(
            response.get("result"), TestSuiteCreated
        )
        res = client.suites._last_res
        assert res.url == client._path("suite/CODE/123")
        assert json.loads(res.request.body) == converter.unstructure(
            update_data
        )


def test_delete_test_suite(client):
    with requests_mock.Mocker() as m:
        m.delete(client._path("suite/CODE/123"), json={"status": True})
        data = client.suites.delete("CODE", 123)
        assert data is None
        res = client.suites._last_res
        assert res.url == client._path("suite/CODE/123")
