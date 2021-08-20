import unittest
from unittest import mock
from argparse import Namespace
from tests.lib.utils import IMAGE, IMAGE_TYPE, RELEASE_NAME
from custom_image_cli.commands.validate_image import ValidateImage


class testValidateImage(unittest.TestCase):

    @mock.patch("custom_image_cli.helper.docker_util.docker_cl.DockerCommand.close_docker")
    @mock.patch("custom_image_cli.helper.docker_util.docker_cl.DockerCommand.__init__")
    @mock.patch("custom_image_cli.commands.validate_image.ValidateImage.initiate")
    @mock.patch("custom_image_cli.validation_tool.validation_helper.validate_all")
    def test_run(self, validate_all, initiate, docker_cmd_constructor, close_docker):
        docker_cmd_constructor.return_value = None
        close_docker.return_value = None
        args = Namespace(local_image_uri=IMAGE, release_name=RELEASE_NAME, image_type=IMAGE_TYPE)

        validate_all.return_value = 3
        validate_image_instance = ValidateImage()
        initiate.return_value = None
        validate_image_instance.set_args(args)
        validate_image_instance.set_docker_command(docker_cmd_constructor)

        self.assertIsNone(validate_image_instance.run())

        validate_all.assert_called_once()

    @mock.patch("custom_image_cli.helper.docker_util.docker_helper.verify_docker")
    @mock.patch("custom_image_cli.helper.docker_util.docker_cl.DockerCommand.docker_inspect")
    @mock.patch("custom_image_cli.helper.docker_util.docker_cl.DockerCommand.__init__")
    @mock.patch("custom_image_cli.helper.manifest_reader.load_yaml")
    @mock.patch("custom_image_cli.helper.logging.Log.info")
    @mock.patch("custom_image_cli.helper.logging.Log.error")
    @mock.patch("custom_image_cli.helper.logging.Log.__init__")
    def test_initialize(self, logger, log_error, log_info,
                        load_yaml, docker_cmd_constructor, docker_inspect, verify_docker):
        validate_image_instance = ValidateImage()

        logger.return_value = None
        log_error.return_value = None
        log_info.return_value = None

        load_yaml.return_value = dict()
        docker_cmd_constructor.return_value = None
        args = Namespace(local_image_uri=IMAGE, release_name=RELEASE_NAME, image_type=IMAGE_TYPE)

        self.assertIsNone(validate_image_instance.initiate(args, logger))
        load_yaml.assert_called_once()

        verify_docker.side_effect = Exception()
        with self.assertRaises(SystemExit) as t:
            validate_image_instance.initiate(args, logger)
        self.assertEqual(t.exception.code, 2)

        verify_docker.side_effect = None
        docker_inspect.side_effect = Exception()
        with self.assertRaises(SystemExit) as t:
            validate_image_instance.initiate(args, logger)
        self.assertEqual(t.exception.code, 2)

        load_yaml.side_effect = Exception()
        with self.assertRaises(SystemExit) as t:
            validate_image_instance.initiate(args, logger)
        self.assertEqual(t.exception.code, 2)
