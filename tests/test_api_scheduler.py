import unittest, datetime
from unittest.mock import patch
import urllib.error
import api_scheduler

class DummyResponse:
    def __init__(self, code=200): self._code = code
    def getcode(self): return self._code
    def __enter__(self): return self
    def __exit__(self, *a): return False

class TestScheduler(unittest.TestCase):
    def test_parse_timestamps(self):
        ts = "09:15:25, 11:58:23\n13:45:09"
        times = api_scheduler.parse_timestamps(ts)
        self.assertEqual(len(times), 3)

    @patch("urllib.request.urlopen")
    def test_call_api_success(self, mock_open):
        mock_open.return_value = DummyResponse(200)
        logger = api_scheduler.configure_logger("test.log")
        res = api_scheduler.call_api(api_scheduler.API_URL, logger, 0)
        self.assertTrue(res)

    @patch("urllib.request.urlopen", side_effect=urllib.error.URLError("fail"))
    def test_call_api_failure(self, mock_open):
        logger = api_scheduler.configure_logger("test.log")
        res = api_scheduler.call_api(api_scheduler.API_URL, logger, 0)
        self.assertFalse(res)

if __name__ == "__main__":
    unittest.main()
