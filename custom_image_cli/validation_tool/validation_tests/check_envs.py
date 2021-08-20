from custom_image_cli.validation_tool.validation_tests import base_check


class CheckEnvs(base_check.BaseCheck):

    def __init__(self, env_path, env_list, env_vars, log):
        self.env_path = env_path
        self.env_list = env_list
        self.env_vars = env_vars
        self.log = log

    def check(self):
        env_variables = {}
        for env in self.env_path:
            var, val = env.split("=")
            env_variables[var] = val
        return self.match(env_variables)

    def match(self, env_variables):
        environment_test = True
        for key in self.env_list:
            env = [env_var for env_var in self.env_vars if env_var.key == key][0]
            if env.env_name in env_variables and env.env_value == env_variables[env.env_name]:
                self.log.info("%s is set with value: %s : PASS" % (env.env_name, env.env_value))
            else:
                self.log.error("%s MUST set to %s : FAIL" % (env.env_name, env.env_value))
                environment_test = False
        return environment_test

    def set_env_path(self, env_path):
        self.env_path = env_path

    def set_manifest_envs(self, env_list):
        self.env_list = env_list
