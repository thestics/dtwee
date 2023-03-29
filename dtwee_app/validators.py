from django.core.exceptions import ValidationError


def unique(model_name, field_name):

    def _unique(value):
        params = {field_name: value}
        if model_name.objects.filter(**params).first() is not None:
            ValidationError(f"{value} is already present in {model_name}")

    return _unique
