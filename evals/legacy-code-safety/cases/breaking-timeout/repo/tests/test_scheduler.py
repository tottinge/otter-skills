import unittest

from scheduler import should_run


class SchedulerTest(unittest.TestCase):
    def test_positive_timeout_waits(self):
        self.assertFalse(should_run({"timeout": "5"}))


if __name__ == "__main__":
    unittest.main()
