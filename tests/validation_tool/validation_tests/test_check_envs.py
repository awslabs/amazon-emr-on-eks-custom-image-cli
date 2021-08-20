import unittest
from unittest import mock
from tests.lib.utils import INSPECT
from custom_image_cli.helper import logging
from custom_image_cli.validation_tool.validation_tests.check_envs import CheckEnvs
from custom_image_cli.validation_tool.validation_models.validation_models import EnvironmentVariable



class TestEnvs(unittest.TestCase):
    def setUp(self) -> None:
        self.log = logging.Log()
        self.inspect = INSPECT
        self.env_list = ["env1", "env2"]
        self.envs = [EnvironmentVariable("env1", "env1", "path1"), EnvironmentVariable("env2", "env2", "path2")]

    def test_match(self):
        env_vars = {'env1': 'path1', 'env2':'path2'}
        env_path = self.inspect['Config']['Env']
        env_check_instance = CheckEnvs(env_path, self.env_list, self.envs, self.log)

        with self.assertLogs(self.log.log) as t:
            result = env_check_instance.match(env_vars)
            self.assertEqual(result, 1)
        expected = 'INFO:logger:env1 is set with value: path1 : PASS'
        self.assertIn(expected, t.output)
        expected = 'INFO:logger:env2 is set with value: path2 : PASS'
        self.assertIn(expected, t.output)

        env_vars['env2'] = 'path3'
        with self.assertLogs(self.log.log) as t:
            result = env_check_instance.match(env_vars)
            self.assertEqual(result, 0)
        expected = 'INFO:logger:env1 is set with value: path1 : PASS'
        self.assertIn(expected, t.output)
        expected = 'ERROR:logger:env2 MUST set to path2 : FAIL'
        self.assertIn(expected, t.output)

    @mock.patch('custom_image_cli.validation_tool.validation_tests.check_envs.CheckEnvs.match')
    def test_check(self, match):
        env_path = self.inspect['Config']['Env']
        env_check_instance = CheckEnvs(env_path, self.env_list, self.envs, self.log)

        match.return_value = 1
        actual = env_check_instance.check()
        expected = {'env1': 'path1', 'env2': 'path2'}
        match.assert_called_once_with(expected)
        self.assertEqual(actual, 1)
