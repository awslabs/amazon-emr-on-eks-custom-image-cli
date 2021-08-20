import unittest
from unittest import mock
from custom_image_cli.helper import logging
from custom_image_cli.validation_tool.validation_tests.check_files import CheckFiles
from custom_image_cli.validation_tool.validation_models.validation_models import FileStructure


class TestCheckFileStructure(unittest.TestCase):
    def setUp(self) -> None:
        self.log = logging.Log()

    @mock.patch('custom_image_cli.helper.docker_util.docker_cl.DockerCommand')
    def test_match(self, docker_constructor):
        docker_cmd = docker_constructor.return_value
        logger = self.log
        docker_cmd.docker_list_files = mock.MagicMock(name="match", return_value=b'something\ntests\nhere\n')
        file_structure_list = ['Test1']
        file_structure = [FileStructure('Test1', '/usr/bin', ['asdfasdf', 'sdfasdf'])]
        file_check_instance = CheckFiles(file_structure_list, file_structure, docker_cmd, 'image_uri', logger)

        file_prefixes = ['test']
        with self.assertLogs(logger.log) as t:
            result = file_check_instance.match('test', 'path', file_prefixes)
            docker_cmd.docker_list_files.assert_called_once()
            self.assertEqual(result, 1)
            expected = 'INFO:logger:File Structure Test for test in path: PASS'
        self.assertIn(expected, t.output)

        file_prefixes = ['test2']
        with self.assertLogs(logger.log) as t:
            expected = "ERROR:logger:test2 MUST be in path : FAIL"
            result = file_check_instance.match('test', 'path', file_prefixes)
            self.assertEqual(result, 0)
        self.assertIn(expected, t.output)

    @mock.patch('custom_image_cli.validation_tool.validation_tests.check_files.CheckFiles.match')
    def test_check(self, match):
        logger = self.log
        match.return_value = 1
        file_structure_list = ['Test1']
        file_structure = [FileStructure('Test1', '/usr/bin', ['asdfasdf', 'sdfasdf'])]
        file_check_instance = CheckFiles(file_structure_list, file_structure, "docker_cmd", 'image_uri', logger)

        actual = file_check_instance.check()
        match.assert_called_once()
        self.assertEqual(actual, 1)

        match.return_value = 0
        actual = file_check_instance.check()
        self.assertEqual(actual, 0)
