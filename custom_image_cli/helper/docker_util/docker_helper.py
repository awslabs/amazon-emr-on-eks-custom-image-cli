import shutil


def verify_docker():
    print("... Checking if docker cli is installed", flush=True)
    shutil.which("docker")