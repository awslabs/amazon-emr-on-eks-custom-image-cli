import unittest
from unittest import mock
from argparse import Namespace
from custom_image_cli.helper import argument_parser
from tests.lib.utils import IMAGE, RELEASE_NAME, IMAGE_TYPE


class TestArgParser(unittest.TestCase):
    @mock.patch("custom_image_cli.helper.argument_parser.ArgsParser")
    def test_arg_parser(self, argsparser):
        args = ["-i", IMAGE, "-r", RELEASE_NAME, "-t", IMAGE_TYPE]
        parser = argsparser.return_value
        parser.add_argument = mock.Mock()
        parser.parse_args = mock.Mock(return_value=Namespace(command='validate-image', local_image_uri=IMAGE,
                                                             release_name=RELEASE_NAME, image_type=IMAGE_TYPE))
        parser_args = argument_parser.parse_commandline_arguments(args)
        parser.add_argument.assert_called()
        parser.parse_args.assert_called_once()
        self.assertEqual(parser_args.local_image_uri, args[1])
        self.assertEqual(parser_args.release_name, args[3])
        self.assertEqual(parser_args.image_type, args[5])
        self.assertEqual(parser_args.command, 'validate-image')
