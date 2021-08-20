import unittest
from tests.lib.utils import RELEASE_NAME, IMAGE_TYPE
from custom_image_cli.helper import logging
from custom_image_cli.validation_tool import check_inputs


class TestInputs(unittest.TestCase):
    def setUp(self) -> None:
        self.release_name = RELEASE_NAME
        self.type = IMAGE_TYPE
        self.log = logging.Log()

    def test_check_version(self):
        self.assertIsNone(check_inputs.check_version(RELEASE_NAME, RELEASE_NAME, self.log))
        expected = "ERROR:logger:No matching image with ReleaseName '%s' : FAIL" % RELEASE_NAME
        with self.assertRaises(SystemExit) as t, self.assertLogs(self.log.log) as m:
            check_inputs.check_version(None, RELEASE_NAME, self.log)
        self.assertEqual(t.exception.code, 2)
        self.assertIn(expected, m.output)

    def test_check_image(self):
        self.assertIsNone(check_inputs.check_image(self.type, self.type, self.log))
        expected = "ERROR:logger:No matching image with Imagetype '%s' : FAIL" % self.type
        with self.assertRaises(SystemExit) as t, self.assertLogs(self.log.log) as m:
            check_inputs.check_image(None, self.type, self.log)
        self.assertEqual(t.exception.code, 2)
        self.assertIn(expected, m.output)

