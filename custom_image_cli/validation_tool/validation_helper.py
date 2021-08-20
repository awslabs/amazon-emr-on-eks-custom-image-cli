from custom_image_cli.validation_tool.validation_tests import check_files, check_envs, check_manifest, check_local_job_run
from custom_image_cli.validation_tool import check_inputs


def validate_all(inspect_result,
              docker_cmd,
              docker_image_uri,
              image_manifest,
              release_name,
              image_type,
              log):
    print("... Checking Image Manifest", flush=True)
    image, file_structure, env_vars = load_validation_info(image_manifest, release_name, image_type, log)

    # tests
    all_tests = [check_manifest.CheckManifest(inspect_result, image.manifest_config, log),
                 check_envs.CheckEnvs(inspect_result['Config']['Env'], image.env_vars, env_vars, log),
                 check_files.CheckFiles(image.file_structures, file_structure, docker_cmd, docker_image_uri, log),
                 check_local_job_run.CheckLocalJobRun(docker_image_uri, docker_cmd, log)]

    result = [test.check() for test in all_tests]
    return all(result)


def load_validation_info(image_manifest, release_name, image_type, log):
    emr_releases = image_manifest.emr_releases
    file_structures = image_manifest.file_structures
    env_vars = image_manifest.env_vars

    # check user inputs
    release = None
    for emr_release in emr_releases:
        if release_name == emr_release.release_name:
            release = emr_release
    check_inputs.check_version(release, release_name, log)

    image = None
    for img in release.images:
        if image_type == img.image_type:
            image = img
    check_inputs.check_image(image, image_type, log)

    return image, file_structures, env_vars
