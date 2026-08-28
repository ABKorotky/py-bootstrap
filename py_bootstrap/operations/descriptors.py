__all__ = ("Descriptor",)

from .build_bootstraps import BuildDescriptor
from .export_bootstraps import ExportDescriptor


class Descriptor(BuildDescriptor, ExportDescriptor): ...
