import unittest
import io
import docker
import shutil
import warnings
from unittest import mock
from custom_image_cli.helper.docker_util.docker_cl import DockerCommand
from custom_image_cli.helper.docker_util.docker_helper import verify_docker
from docker.models.containers import Container


class TestDockers(unittest.TestCase):
    def setUp(self) -> None:
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        docker.from_env = mock.Mock(return_value=docker.client.DockerClient())
        self.docker_cmd = DockerCommand()
        docker.from_env.assert_called_once()

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_verify_docker(self, mock_stdout):
        shutil.which = mock.Mock()
        verify_docker()
        expected = "... Checking if docker cli is installed\n"
        self.assertEqual(expected, mock_stdout.getvalue())
        shutil.which.assert_called_once_with("docker")

    def test_docker_inspect(self):
        self.docker_cmd.client.api.inspect_image = mock.Mock(return_value=dict())
        actual = self.docker_cmd.docker_inspect("image")
        self.assertEqual(actual, {})
        self.docker_cmd.client.api.inspect_image.assert_called()

    @mock.patch.object(docker.models.containers.ContainerCollection, "run")
    def test_docker_container(self, run):
        run.return_value = docker.models.containers.Container()
        actual = self.docker_cmd.create_container("image")
        self.assertIsInstance(actual, Container)
        self.docker_cmd.client.containers.run.assert_called_once()

    def test_docker_run(self):
        self.docker_cmd.create_container = mock.Mock(return_value=docker.models.containers.Container())
        self.docker_cmd.container = self.docker_cmd.create_container()
        self.docker_cmd.container.exec_run = \
            mock.Mock(return_value=docker.models.containers.ExecResult(exit_code=0, output=b'something'))
        actual = self.docker_cmd.docker_run("image", "command")
        self.assertEqual(actual, docker.models.containers.ExecResult(exit_code=0, output=b'something'))
        self.docker_cmd.container.exec_run.assert_called_once()

    def test_docker_list(self):
        self.docker_cmd.create_container = mock.Mock(return_value=docker.models.containers.Container())
        self.docker_cmd.container = self.docker_cmd.create_container()
        self.docker_cmd.create_container.assert_called_once()

        self.docker_cmd.container.exec_run = \
            mock.Mock(return_value=docker.models.containers.ExecResult(exit_code=0, output=b'something'))
        actual = self.docker_cmd.docker_list_files('somathing', '/usr/bin')
        self.assertIsInstance(actual, bytes)
        self.assertEqual(actual, b'something')
        self.docker_cmd.container.exec_run.assert_called_once()

    def test_docker_close(self):
        self.docker_cmd.create_container = mock.Mock(return_value=docker.models.containers.Container())
        self.docker_cmd.container = self.docker_cmd.create_container()
        self.docker_cmd.create_container.assert_called_once()

        self.docker_cmd.container.stop = mock.Mock()
        self.docker_cmd.container.remove = mock.Mock()
        self.docker_cmd.client.close = mock.Mock()
        actual = self.docker_cmd.close_docker()
        self.assertIsNone(actual)
        self.docker_cmd.container.stop.assert_called_once()
        self.docker_cmd.container.remove.assert_called_once()
        self.docker_cmd.client.close.assert_called_once()

