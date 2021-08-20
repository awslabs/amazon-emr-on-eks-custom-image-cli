from custom_image_cli.validation_tool.validation_tests import base_check


class CheckManifest(base_check.BaseCheck):

    def __init__(self, inspect_result, manifest_config, log):
        self.inspect_result = inspect_result
        self.manifest_config = manifest_config
        self.log = log

    def check(self):
        manifest_validation_test = True

        image_id = self.inspect_result['Id'].split(":")[1]

        self.log.info("Image ID: %s" % image_id)
        self.log.info("Created On: %s" % self.inspect_result['Created'])

        # test username
        username = self.inspect_result['Config']['User']
        target_username = self.manifest_config.user
        if username == target_username:
            self.log.info("Default User Set to %s : PASS" % target_username)
        else:
            self.log.error("Default User MUST be %s. Set to %s : FAIL" % (target_username, username))
            manifest_validation_test = False

        # test workingDir
        working_dir = self.inspect_result['Config']['WorkingDir']
        target_working_dir = self.manifest_config.working_dir
        if working_dir == target_working_dir:
            self.log.info("Working Directory Set to %s : PASS" % target_working_dir)
        else:
            self.log.error("Working Directory MUST be %s. Set to %s : FAIL" % (target_working_dir, working_dir))
            manifest_validation_test = False

        # test entrypoint
        entrypoint = self.inspect_result['Config']['Entrypoint'][0]
        target_entrypoint = self.manifest_config.entrypoint
        if entrypoint == target_entrypoint:
            self.log.info("Entrypoint Set to %s : PASS" % target_entrypoint)
        else:
            self.log.error("Entrypoint MUST be %s. Set to %s : FAIL" % (target_entrypoint, entrypoint))
            manifest_validation_test = False

        return manifest_validation_test

    def set_inspect_result(self, inspect):
        self.inspect_result = inspect

    def set_manifest_config(self, manifest_config):
        self.manifest_config = manifest_config
