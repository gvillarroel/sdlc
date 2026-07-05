import io
import unittest
import urllib.error
from unittest.mock import patch

from scripts.refresh_github_metadata import get_json, metadata_rows


class GitHubMetadataRefreshTest(unittest.TestCase):
    def test_metadata_rows_passes_token_and_compares_license(self):
        calls = []
        raw_data = {
            "alternatives": [
                {
                    "id": "example",
                    "name": "Example",
                    "repo": "owner/repo",
                    "stars": 10,
                    "last_pushed_at": "2026-07-01",
                    "license": "MIT",
                }
            ]
        }

        def fake_get_json(url, timeout, github_token="", attempts=2):
            calls.append((url, timeout, github_token, attempts))
            if url.endswith("/releases/latest"):
                return {"tag_name": "v1.0.0"}, ""
            return {
                "stargazers_count": 12,
                "pushed_at": "2026-07-05T12:00:00Z",
                "license": {"spdx_id": "MIT"},
                "archived": False,
            }, ""

        with patch("scripts.refresh_github_metadata.get_json", fake_get_json):
            rows = metadata_rows(
                raw_data,
                timeout=20,
                sleep_seconds=0,
                github_token="token",
            )

        self.assertEqual({call[2] for call in calls}, {"token"})
        self.assertEqual(rows[0]["live_stars"], 12)
        self.assertEqual(rows[0]["star_delta"], 2)
        self.assertTrue(rows[0]["license_matches"])
        self.assertEqual(rows[0]["latest_release_tag"], "v1.0.0")

    def test_get_json_retries_without_invalid_token(self):
        calls = []

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b'{"ok": true}'

        def fake_urlopen(request, timeout):
            headers = dict(request.header_items())
            calls.append(headers.get("Authorization", ""))
            if len(calls) == 1:
                raise urllib.error.HTTPError(
                    request.full_url,
                    401,
                    "Unauthorized",
                    hdrs=None,
                    fp=io.BytesIO(b""),
                )
            return FakeResponse()

        with patch("scripts.refresh_github_metadata.urllib.request.urlopen", fake_urlopen):
            payload, error = get_json(
                "https://api.github.com/repos/example/repo",
                timeout=20,
                github_token="invalid",
                attempts=2,
            )

        self.assertEqual(payload, {"ok": True})
        self.assertEqual(error, "")
        self.assertEqual(calls, ["Bearer invalid", ""])


if __name__ == "__main__":
    unittest.main()
