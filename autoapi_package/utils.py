from django.db.models.options import Options


def get_model_key(opts: Options) -> str:
    return f"{opts.app_label}.{opts.model_name}"
