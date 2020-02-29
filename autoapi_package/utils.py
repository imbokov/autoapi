from importlib import import_module
from typing import List, Type

from django.db.models.options import Options


def get_model_key(opts: Options) -> str:
    return f"{opts.app_label}.{opts.model_name}"


def get_field_names(opts: Options) -> List[str]:
    return [field.name for field in opts.get_fields()]


def get_class(path: str) -> Type:
    split_path = path.split(".")
    module_path = ".".join(split_path[:-1])
    class_name = split_path[-1]
    # The attribute getter is not defensive on purpose.
    return getattr(import_module(module_path), class_name)
