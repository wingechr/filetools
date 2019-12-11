import os
from .tools import Dict


def get_file_types_hierarchy(file_type):
    """Return all file types from the hierarchy"""
    types = [""]  # root
    if file_type:
        parts = file_type.split("/")
        for i in range(len(parts)):
            types.append("/".join(parts[: i + 1]))
    return types


class FileTool:
    def __init__(self, **user_settings):
        """

        Args:
            user_settings: dictionary of user settings overriding the defaults
        """
        self.config = {}
        self.config.update(user_settings)
        self.resource_classes = Dict(allow_overwrite=False)
        self.file_inspector_classes = Dict()
        # register the root file type
        self.register_file_class(FileBinary)

    def identify_file(self, path, file_type=""):
        """Identify a file.

        Args:
            path: Path like object describing the location
            file_type (str): file type identifier
                             like "text/json" or "text/image/jpg"
        Returns:
            FileResource class that matches the file
        """

        for ftype in reversed(get_file_types_hierarchy(file_type)):
            resource_class = self.resource_classes.get(ftype)
            if resource_class:
                return resource_class
        raise Exception("No FileResource matching '%s'" % file_type)

    def inspect_file(self, path):
        """Identify a file.

        Args:
            path: Path like object describing the location
        Returns:
            dict like with key value pairs of meta data
            provided by the inspector classes
        """
        file_resource_class = self.identify_file(path)
        file_type = file_resource_class.file_type
        # get all the registered inspectors that are appropriate
        # for this file type OR any one above that in the hierarchy,
        # i.e. "text/csv" also gets information from "text"
        # starting from the top
        meta_all = Dict(get_key=lambda x: str(x).lower() if x else "")
        for ftype in get_file_types_hierarchy(file_type):
            for insp in self.file_inspector_classes.get(ftype, []):
                meta = insp.inspect_file(str(path))
                meta_all.update(meta)
        return meta_all

    def register_file_resource_class(self, file_resource_class):
        """Register a new class based on FileResource

        Args:
            file_resource_class: subclass of FileResource
        """
        ftype = file_resource_class.file_type
        self.resource_classes[ftype] = file_resource_class

    def register_file_inspector_class(self, file_inspector_class):
        """Register a new class based on FileResource

        Args:
            file_inspector_class: subclass of FileInspector
        """
        for ftype in file_inspector_class.file_types:
            self.file_inspector_classes.get(ftype, set(), add_on_missing=True).add(
                file_inspector_class
            )

    def register_file_class(self, file_class):
        if not issubclass(file_class, FileBase):
            raise Exception("file_class must be subclass of FileBase")
        if issubclass(file_class, FileResource):
            self.register_file_resource_class(file_class)
        if issubclass(file_class, FileInspector):
            self.register_file_inspector_class(file_class)


class FileBase:
    pass


class FileResource(FileBase):
    file_type = None  # path like identifier, e.g. /text/json or /text/image/jpg


class FileInspector(FileBase):
    # :param file_types: blabla
    file_types = None

    @classmethod
    def inspect_file(cls, path):
        """Identify a file.

        Args:
            path (str): path to file
        Returns:
            dict with key value pairs of meta data
        """
        return {}


class FileBinary(FileResource, FileInspector):
    file_type = ""
    file_types = [""]

    @classmethod
    def inspect_file(cls, path):
        """Identify a file.

        Args:
            path (str): path to file
        Returns:
            dict with key value pairs of meta data
        """
        return {"size_bytes": cls.get_size(path)}

    @classmethod
    def get_size(cls, path):
        return os.path.getsize(path)


class Config:
    pass


class Path:
    pass
