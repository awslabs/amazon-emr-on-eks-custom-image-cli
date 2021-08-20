import yaml


class ImageManifest(yaml.YAMLObject):
    yaml_tag = u'!ImageManifest'

    # emr_releases: list['EmrRelease'], files_structures: list['FileStructure'], env_vars: list['EnvironmentVariable']
    def __init__(self, emr_releases, files_structures, env_vars):
        self.emr_releases = emr_releases
        self.file_structures = files_structures
        self.env_vars = env_vars

    def to_dict(self):
        return {'EmrReleases': self.emr_releases,
                'FileStructures': self.file_structures,
                'EnvironmentVariables': self.env_vars}

    @classmethod
    def to_yaml(cls, dumper, data):
        data.__dict__ = data.to_dict()
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls)

    @classmethod
    def from_yaml(cls, loader, node):
        for data in loader.construct_yaml_map(node):
            pass
        emr_releases = data['EmrReleases']
        file_structure = data['FileStructures']
        env_vars = data['EnvironmentVariables']
        return cls(emr_releases, file_structure, env_vars)


class EmrRelease(yaml.YAMLObject):
    yaml_tag = u'!EmrRelease'

    # release_name: str, images: list['ImageDetail']
    def __init__(self, release_name, images):
        self.release_name = release_name
        self.images = images

    def to_dict(self):
        return {'ReleaseName': self.release_name,
                'Images': self.images}

    @classmethod
    def to_yaml(cls, dumper, data):
        data.__dict__ = data.to_dict()
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls)

    @classmethod
    def from_yaml(cls, loader, node):
        for data in loader.construct_yaml_map(node):
            pass
        release_name = data['ReleaseName']
        images = data['Images']
        return cls(release_name, images)


class EnvironmentVariable(yaml.YAMLObject):
    yaml_tag = u'!EnvironmentVariable'

    # key: str, env_name: str, env_value: str
    def __init__(self, key, env_name, env_value):
        self.key = key
        self.env_name = env_name
        self.env_value = env_value

    def to_dict(self):
        return {'Key': self.key,
                'EnvName': self.env_name,
                'EnvValue': self.env_value}

    @classmethod
    def to_yaml(cls, dumper, data):
        data.__dict__ = data.to_dict()
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls)

    @classmethod
    def from_yaml(cls, loader, node):
        for data in loader.construct_yaml_map(node):
            pass
        key = data['Key']
        env_name = data['EnvName']
        env_value = data['EnvValue']
        return cls(key, env_name, env_value)


class FileStructure(yaml.YAMLObject):
    yaml_tag = u'!FileStructure'

    # name: str, relative_location: str, file_prefixes: list[str]
    def __init__(self, name, relative_location, file_prefixes):
        self.name = name
        self.relative_location = relative_location
        self.file_prefixes = file_prefixes

    def to_dict(self):
        return {'Name': self.name,
                'RelativeLocation': self.relative_location,
                'FilePrefixes': self.file_prefixes}

    @classmethod
    def to_yaml(cls, dumper, data):
        data.__dict__ = data.to_dict()
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls)

    @classmethod
    def from_yaml(cls, loader, node):
        for data in loader.construct_yaml_map(node):
            pass
        name = data['Name']
        relative_location = data['RelativeLocation']
        file_prefixes = data['FilePrefixes']
        return cls(name, relative_location, file_prefixes)


class ImageDetail(yaml.YAMLObject):
    yaml_tag = u'!ImageDetail'

    # image_type: str, manifest_config: 'ManifestConfig', env_vars: list[str], file_structures: list[str]
    def __init__(self, image_type, manifest_config, env_vars, file_structures):
        self.image_type = image_type
        self.manifest_config = manifest_config
        self.env_vars = env_vars
        self.file_structures = file_structures

    def to_dict(self):
        return {'ImageType': self.image_type,
                'ManifestConfig': self.manifest_config,
                'EnvironmentVariable': self.env_vars,
                'FileStructure': self.file_structures}

    @classmethod
    def to_yaml(cls, dumper, data):
        data.__dict__ = data.to_dict()
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls)

    @classmethod
    def from_yaml(cls, loader, node):
        for data in loader.construct_yaml_map(node):
            pass
        image_type = data['ImageType']
        manifest_config = data['ManifestConfig']
        env_vars = data['EnvironmentVariable']
        file_structures = data['FileStructure']
        return cls(image_type, manifest_config, env_vars, file_structures)


class ManifestConfig(yaml.YAMLObject):
    yaml_tag = u'!ManifestConfig'

    # entrypoint: str, user: str, working_dir: str
    def __init__(self, entrypoint, user, working_dir):
        self.entrypoint = entrypoint
        self.user = user
        self.working_dir = working_dir

    def to_dict(self):
        return {'Entrypoint': self.entrypoint,
                'User': self.user,
                'WorkingDir': self.working_dir}

    @classmethod
    def to_yaml(cls, dumper, data):
        data.__dict__ = data.to_dict()
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls)

    @classmethod
    def from_yaml(cls, loader, node):
        for data in loader.construct_yaml_map(node):
            pass
        entrypoint = data['Entrypoint']
        user = data['User']
        working_dir = data['WorkingDir']
        return cls(entrypoint, user, working_dir)
