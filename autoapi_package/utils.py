from typing import List

from django.db.models.options import Options


def get_model_key(opts: Options) -> str:
    return f"{opts.app_label}.{opts.model_name}"


def get_field_names(opts: Options) -> List[str]:
    return [field.name for field in opts.get_fields()]
