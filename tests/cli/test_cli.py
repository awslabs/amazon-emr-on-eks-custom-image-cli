import unittest
from unittest import mock
from argparse import Namespace
from tests.lib.utils import IMAGE, IMAGE_TYPE, RELEASE_NAME
from custom_image_cli.cli import cli


class TestCli(unittest.TestCase):

    @mock.patch("custom_image_cli.helper.print_message.print_pre_verification_text")
    @mock.patch("custom_image_cli.helper.argument_parser.parse_commandline_arguments")
    @mock.patch("custom_image_cli.commands.validate_image.ValidateImage.run")
    @mock.patch("custom_image_cli.commands.validate_image.ValidateImage.initiate")
    @mock.patch("custom_image_cli.commands.validate_image.ValidateImage.__init__")
    def test_run_validate_image(self, validate_image_constructor, validate_image_initiate, validate_image_run,
                                parse_args, print_pre):
        validate_image_constructor.return_value = None
        validate_image_initiate.return_value = None
        validate_image_run.return_value = None

        parse_args.return_value = Namespace(local_image_uri=IMAGE, release_name=RELEASE_NAME,
                                            image_type=IMAGE_TYPE, command='validate-image')
        self.assertIsNone(cli.run())

        print_pre.assert_called_once()
        validate_image_initiate.assert_called_once()
        validate_image_run.assert_called_once()
        parse_args.assert_called_once()
