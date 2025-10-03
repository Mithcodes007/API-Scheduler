import unittest, os
from api_scheduler import call_api, configure_logger

class Integration(unittest.TestCase):
    def test_real_call(self):
        if not os.environ.get("RUN_INTEGRATION"):
            self.skipTest("Set RUN_INTEGRATION=1 to run")
        logger = configure_logger("integration.log")
        self.assertTrue(call_api("https://ifconfig.co/json", logger, 0))

if __name__ == "__main__":
    unittest.main()
