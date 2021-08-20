import unittest
import io
from custom_image_cli import __version__
from unittest import mock
from custom_image_cli.helper import print_message


class TestPrintMessage(unittest.TestCase):
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_pre(self, mock_stdout):
        expected = "Amazon EMR on EKS - Custom Image CLI\nVersion: %s\n" % __version__
        print_message.print_pre_verification_text()
        self.assertEqual(mock_stdout.getvalue(), expected)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_validate_completion_msg_succeed(self, mock_stdout):
        expected = "-----------------------------------------------------------------\n" \
                    "Overall Custom Image Validation Succeeded.\n" \
                    "-----------------------------------------------------------------\n"
        print_message.print_validate_completion_message(True)
        self.assertEqual(mock_stdout.getvalue(), expected)


    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_validate_completion_msg_fail(self, mock_stdout):
        expected = "-----------------------------------------------------------------\n" \
                    "Custom Image Validation Failed. Please see individual test results above for detailed information.\n" \
                    "-----------------------------------------------------------------\n"
        print_message.print_validate_completion_message(False)
        self.assertEqual(mock_stdout.getvalue(), expected)


