import unittest
from tests.lib.utils import INSPECT
from custom_image_cli.helper import logging
from custom_image_cli.validation_tool.validation_tests.check_manifest import CheckManifest
from custom_image_cli.validation_tool.validation_models.validation_models import ManifestConfig


class TestManifest(unittest.TestCase):
    def setUp(self) -> None:
        self.log = logging.Log()
        self.inspect = INSPECT
        self.manifest_config = ManifestConfig("entrypoint", "user", "workingdir")

    def test_check_manifest(self):
        with self.assertLogs(self.log.log) as l:
            manifest_check_instance = CheckManifest(self.inspect, self.manifest_config, self.log)
            result = manifest_check_instance.check()
            self.assertEqual(result, True)
        expected = ['INFO:logger:Image ID: %s' % self.inspect['Id'].split(":")[1],
                    'INFO:logger:Created On: %s' % self.inspect['Created'],
                    'INFO:logger:Default User Set to %s : PASS' % self.manifest_config.user,
                    'INFO:logger:Working Directory Set to %s : PASS' % self.manifest_config.working_dir,
                    'INFO:logger:Entrypoint Set to %s : PASS' % self.manifest_config.entrypoint]
        self.assertEqual(expected, l.output)

        self.inspect['Config']['User'] = 'other'
        self.inspect['Config']['WorkingDir'] = 'other'
        self.inspect['Config']['Entrypoint'][0] = 'other'
        with self.assertLogs(self.log.log) as l:
            manifest_check_instance.set_inspect_result(self.inspect)
            result = manifest_check_instance.check()
            self.assertEqual(result, False)

        expected = ['INFO:logger:Image ID: %s' % self.inspect['Id'].split(":")[1],
                    'INFO:logger:Created On: %s' % self.inspect['Created'],
                    'ERROR:logger:Default User MUST be %s. Set to %s : FAIL'
                    % (self.manifest_config.user, self.inspect['Config']['User']),
                    'ERROR:logger:Working Directory MUST be %s. Set to %s : FAIL'
                    % (self.manifest_config.working_dir, self.inspect['Config']['WorkingDir']),
                    'ERROR:logger:Entrypoint MUST be %s. Set to %s : FAIL'
                    % (self.manifest_config.entrypoint, self.inspect['Config']['Entrypoint'][0])]
        self.assertEqual(expected, l.output)

