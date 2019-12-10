
class FileTool:
    def __init__(self, **user_settings):
        """

        :param user_settings: dictionary of user settings overriding the defaults
        """
        self.config = {}
        self.config.update(user_settings)
        self.resource_classes = []
        self.file_inspector_classes = []

    def identify_file(self, path):
        """Identify a file.

        :param path: Path like object describing the location
        :return: FileResource class that matches the file
        """
        raise NotImplementedError

    def inspect_file(self, path):
        """Identify a file.

        :param path: Path like object describing the location
        :return: dict with key value pairs of meta data provided by the inspector classes
        """
        fr = self.identify_file(path)


    def register_file_resource_class(self, file_resource_class):
        """Register a new class based on FileResource
        :param file_resource_class: subclass of FileResource
        """
        self.resource_classes.append(file_resource_class)

    def register_file_inspector_class(self, file_inspector_class):
        """Register a new class based on FileResource
        :param file_inspector_class: subclass of FileInspector
        """
        self.file_inspector_classes.append(file_inspector_class)


class FileResource:
    pass


class FileInspector:
    # :param file_types: blabla
    file_types = []



class Config:
    pass


class Path:
    pass
