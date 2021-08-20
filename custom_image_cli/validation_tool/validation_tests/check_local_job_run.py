from docker.errors import ContainerError
from custom_image_cli.validation_tool.validation_tests import base_check


class CheckLocalJobRun(base_check.BaseCheck):

    def __init__(self, image_uri, docker_cmd, log):
        self.image_uri = image_uri
        self.docker_cmd = docker_cmd
        self.log = log
        self.entry_point = 'local:///usr/lib/spark/examples/jars/spark-examples.jar'

    def check(self):
        try:
            print('... Start Running Sample Spark Job')
            command = ['bash', 'spark-submit ' \
                               '--deploy-mode client ' \
                               '--master local ' \
                               '--class org.apache.spark.examples.SparkPi ' + self.entry_point]
            self.docker_cmd.docker_run(self.image_uri, command)
        except ContainerError:
            self.log.error('Sample Spark Job Test with %s : FAIL' % self.entry_point)
            return False
        self.log.info('Sample Spark Job Test with %s : PASS' % self.entry_point)
        return True
