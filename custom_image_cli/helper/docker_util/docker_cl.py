import docker


class DockerCommand:
    def __init__(self):
        self.client = docker.from_env()
        self.container = None

    def create_container(self, docker_image_uri):
        return self.client.containers.run(image=docker_image_uri, command="/bin/bash", detach=True, tty=True)

    def docker_list_files(self, docker_image_uri, path):
        command = ['bash', '-c', 'ls -al %s | awk \'{print $9}\'' % path]
        result = self.docker_run(docker_image_uri, command)
        return result.output

    def docker_inspect(self, docker_image_uri):
        return self.client.api.inspect_image(docker_image_uri)

    def docker_run(self, image_uri, command):
        if self.container is None:
            self.container = self.create_container(image_uri)
        return self.container.exec_run(command)

    def close_docker(self):
        if self.container is not None:
            self.container.stop(timeout=0)
            self.container.remove()
        self.client.close()
