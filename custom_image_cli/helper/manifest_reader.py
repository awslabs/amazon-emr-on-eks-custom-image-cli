import yaml
from custom_image_cli.validation_tool.validation_models.validation_models import ImageManifest

yaml.add_constructor(ImageManifest.yaml_tag, ImageManifest.from_yaml)


def load_yaml(file):
    with open(file, "r") as f:
        image_manifest = yaml.load(f, Loader=yaml.Loader)
        return image_manifest
