from custom_image_cli.commands import base_command
import sys, os
from custom_image_cli.helper.docker_util import docker_helper, docker_cl
from custom_image_cli.helper import manifest_reader
from custom_image_cli.validation_tool import validation_helper
from custom_image_cli.helper.print_message import print_validate_completion_message

# Check if this is an executable.
if getattr(sys, 'frozen', False):
    IMAGE_MANIFEST_YAML = sys._MEIPASS + "/assets/image-manifest.yaml"
else:
    curr_dir = os.path.dirname(__file__)
    IMAGE_MANIFEST_YAML = os.path.join(curr_dir, "../../assets/image-manifest.yaml")


class ValidateImage(base_command.BaseCommand):

    def __init__(self):
        self.args = None
        self.log = None
        self.test_num = None
        self.image_manifest = None
        self.docker_cmd = None
        self.inspect_result = None

    def initiate(self, args, log, test_num=3):
        self.args = args
        self.log = log
        self.test_num = test_num
        # load image manifest
        try:
            self.image_manifest = manifest_reader.load_yaml(IMAGE_MANIFEST_YAML)
        except Exception as e:
            print(e)
            self.log.error("image-manifest.yaml doesn't exist and is required.")
            sys.exit(2)

        # initialize docker
        try:
            docker_helper.verify_docker()
            self.docker_cmd = docker_cl.DockerCommand()
        except Exception:
            self.log.error("docker cli doesn't exist but is required.")
            sys.exit(2)

        # inspect image
        try:
            self.inspect_result = self.docker_cmd.docker_inspect(args.local_image_uri)
        except Exception:
            self.log.error("No such image found.")
            sys.exit(2)

        # set default runtime image type to spark
        if self.args.image_type is None:
            self.args.image_type = 'spark'

    def run(self):
        validation_succeeded = validation_helper.validate_all(self.inspect_result,
                                                              self.docker_cmd,
                                                              self.args.local_image_uri,
                                                              self.image_manifest,
                                                              self.args.release_name,
                                                              self.args.image_type,
                                                              self.log)
        self.docker_cmd.close_docker()
        print_validate_completion_message(validation_succeeded)

    def set_args(self, args):
        self.args = args

    def set_docker_command(self, docker_command):
        self.docker_cmd = docker_command
