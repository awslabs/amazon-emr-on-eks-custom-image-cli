"""
Define testing utils
"""

IMAGE = "895885662937.dkr.ecr.us-west-2.amazonaws.com/spark/emr-5.32.0-20210129:2.4.7-amzn-0-vanilla"
RELEASE_NAME = "emr-5.32"
IMAGE_TYPE = "spark"

INSPECT = dict()
INSPECT['Id'] = 'sha:asdf'
INSPECT['Created'] = '2020/04/22'
INSPECT['Config'] = dict()
INSPECT['Config']['User'] = 'user'
INSPECT['Config']['WorkingDir'] = 'workingdir'
INSPECT['Config']['Entrypoint'] = ['entrypoint']
INSPECT['Config']['Env'] = ['env1=path1', "env2=path2"]
