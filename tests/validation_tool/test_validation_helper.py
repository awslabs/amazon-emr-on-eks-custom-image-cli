import unittest
import io
from unittest import mock
from tests.lib.utils import INSPECT
from custom_image_cli.validation_tool import validation_helper
from custom_image_cli.validation_tool.validation_models.validation_models import \
    ImageDetail, ImageManifest, EmrRelease


class TestValidationHelper(unittest.TestCase):
    def setUp(self) -> None:
        self.inspect = INSPECT
        self.manifest = ImageManifest([EmrRelease("release_name", [ImageDetail("image_type", None, [], [])])], [], [])

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('custom_image_cli.validation_tool.validation_helper.load_validation_info')
    @mock.patch("custom_image_cli.validation_tool.validation_tests.check_local_job_run.CheckLocalJobRun.check")
    @mock.patch("custom_image_cli.validation_tool.validation_tests.check_manifest.CheckManifest.check")
    @mock.patch("custom_image_cli.validation_tool.validation_tests.check_manifest.CheckManifest.__init__")
    @mock.patch("custom_image_cli.validation_tool.validation_tests.check_files.CheckFiles.check")
    @mock.patch("custom_image_cli.validation_tool.validation_tests.check_files.CheckFiles.__init__")
    @mock.patch("custom_image_cli.validation_tool.validation_tests.check_envs.CheckEnvs.check")
    @mock.patch("custom_image_cli.validation_tool.validation_tests.check_envs.CheckEnvs.__init__")
    def test_validate_all(self, check_envs_constructor, check_envs, check_files_constructor,
                          check_files, check_manifest_constructor,
                          check_manifest, check_local_job_run, load_info, mock_stdout):
        check_envs_constructor.return_value = None
        check_envs.return_value = True
        check_files_constructor.return_value = None
        check_files.return_value = True
        check_manifest_constructor.return_value = None
        check_manifest.return_value = True
        check_local_job_run.return_value = True
        load_info.return_value = ImageDetail("image_type", None, [], []), [], []

        actual = validation_helper.validate_all(self.inspect, "docker_cmd", "docker_image_uri",
                                                self.manifest, "release_name", "image_type", "log")
        self.assertEqual(actual, True)

        check_manifest.assert_called_once()
        check_envs.assert_called_once()
        check_files.assert_called_once()
        check_local_job_run.assert_called_once()

        expected = "... Checking Image Manifest\n"
        self.assertEqual(expected, mock_stdout.getvalue())

    @mock.patch("custom_image_cli.validation_tool.check_inputs.check_version")
    @mock.patch("custom_image_cli.validation_tool.check_inputs.check_image")
    def test_load_validation_info(self, check_image, check_version):
        value = self.manifest
        check_version.return_value = None
        check_image.return_value = None

        actual_img, actual_file, actual_env = validation_helper.load_validation_info(self.manifest, "release_name", "image_type", "log")
        self.assertEqual(actual_img, self.manifest.emr_releases[0].images[0])
        self.assertEqual(actual_file, [])
        self.assertEqual(actual_env, [])

        check_version.assert_called_once_with(self.manifest.emr_releases[0], "release_name", "log")
        check_image.assert_called_once_with(self.manifest.emr_releases[0].images[0], "image_type", "log")
