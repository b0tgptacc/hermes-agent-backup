from __future__ import annotations

import importlib.util
import pathlib
import socket
import unittest
from unittest import mock

MODULE_PATH = pathlib.Path(__file__).with_name("recover_page.py")
SPEC = importlib.util.spec_from_file_location("recover_page", MODULE_PATH)
assert SPEC and SPEC.loader
recover_page = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recover_page)


class TargetBoundaryTests(unittest.TestCase):
    def assert_rejected_without_route(self, url: str) -> None:
        route = mock.Mock(return_value=None)
        with mock.patch.object(recover_page, "ROUTES", (route,)):
            with self.assertRaises(ValueError):
                recover_page.recover(url)
        route.assert_not_called()

    def test_rejects_private_and_metadata_literals(self) -> None:
        for url in (
            "http://127.0.0.1/a",
            "http://[::1]/a",
            "http://10.0.0.1/a",
            "http://169.254.169.254/latest/meta-data",
            "http://192.168.1.5/a",
        ):
            with self.subTest(url=url):
                self.assert_rejected_without_route(url)

    def test_rejects_intranet_names_and_userinfo(self) -> None:
        for url in (
            "https://localhost/a",
            "https://service.internal/a",
            "https://printer.local/a",
            "https://intranet/a",
            "https://user:password@example.com/a",
        ):
            with self.subTest(url=url):
                self.assert_rejected_without_route(url)

    def test_rejects_signed_or_secret_query_keys(self) -> None:
        for url in (
            "https://example.com/file?token=abc",
            "https://example.com/file?X-Amz-Signature=abc",
            "https://example.com/file?sig=abc",
            "https://example.com/file?access_token=abc",
            "https://example.com/file?Expires=123",
        ):
            with self.subTest(url=url):
                self.assert_rejected_without_route(url)

    def test_rejects_hostname_resolving_private(self) -> None:
        private_answer = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.1.2.3", 443))]
        with mock.patch.object(recover_page.socket, "getaddrinfo", return_value=private_answer):
            self.assert_rejected_without_route("https://public-looking.example/page")

    def test_public_url_may_reach_route(self) -> None:
        public_answer = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]
        route = mock.Mock(return_value={"route": "test"})
        with mock.patch.object(recover_page.socket, "getaddrinfo", return_value=public_answer), mock.patch.object(
            recover_page, "ROUTES", (route,)
        ):
            self.assertEqual({"route": "test"}, recover_page.recover("https://example.com/public?id=7"))
        route.assert_called_once()


if __name__ == "__main__":
    unittest.main()
