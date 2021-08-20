import unittest
from unittest import mock

from docker.errors import ContainerError

from custom_image_cli.helper import logging
from custom_image_cli.validation_tool.validation_tests.check_local_job_run import CheckLocalJobRun


class TestCheckLocalSparkJob(unittest.TestCase):
    def setUp(self) -> None:
        self.log = logging.Log()

    @mock.patch('custom_image_cli.helper.docker_util.docker_cl.DockerCommand')
    def test_check(self, docker_constructor):
        docker_cmd = docker_constructor.return_value
        logger = self.log
        sanity_check_instance = CheckLocalJobRun('image_uri', docker_cmd, logger)

        docker_cmd.docker_run = mock.Mock(return_value=None)
        with self.assertLogs(logger.log) as t:
            result = sanity_check_instance.check()
            docker_cmd.docker_run.assert_called_once()
            self.assertEqual(result, 1)
        expected = 'INFO:logger:Sample Spark Job Test with ' \
                   'local:///usr/lib/spark/examples/jars/spark-examples.jar : PASS'
        self.assertIn(expected, t.output)

        docker_cmd.docker_run.side_effect = ContainerError(None, '', '', '', None)
        with self.assertLogs(logger.log) as t:
            result = sanity_check_instance.check()
            self.assertEqual(result, 0)
        expected = 'ERROR:logger:Sample Spark Job Test with ' \
                   'local:///usr/lib/spark/examples/jars/spark-examples.jar : FAIL'
        self.assertIn(expected, t.output)
