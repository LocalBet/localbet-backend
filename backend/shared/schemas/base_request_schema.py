"""
BaseRequestSchema module.
"""

from types import NoneType
from typing import Any

from pydantic import BaseModel

from backend.shared.infrastructure.errors import ExtraFieldsError, MissingFieldsError


class BaseRequestSchema(BaseModel):
    """
    BaseRequestSchema class.
    """

    def __init__(self, **data: dict[str, Any]) -> None:  # noqa: C901
        """
        BaseRequestSchema constructor.

        Args:
            data (dict[str, Any]): Data to initialize the model.
        """
        provided_fields = set(data.keys())

        model_fields = set(self.__class__.model_fields.keys())
        model_aliases = {field: self.__class__.model_fields[field].serialization_alias for field in model_fields}
        model_types = {field: self.__class__.model_fields[field].annotation for field in model_fields}
        model_defaults = {
            field: self.__class__.model_fields[field].default
            for field in model_fields
            if self.__class__.model_fields[field].default is not None
        }

        missing_fields = model_fields - provided_fields
        for field in missing_fields.copy():
            # If the field defines a default factory, call it and fill the value.
            # This is necessary because this constructor uses `model_construct`
            # which does not run Pydantic's default factories automatically.
            field_info = self.__class__.model_fields[field]
            default_factory = getattr(field_info, "default_factory", None)
            if default_factory is not None:
                provided_fields.add(field)
                # call the factory to obtain the default value
                data[field] = default_factory()
                missing_fields.remove(field)
                continue
            if field in model_types:
                if model_aliases[field] in data:
                    # Convert the alias to the original field name
                    provided_fields.add(field)
                    provided_fields.remove(model_aliases[field])  # type: ignore[arg-type]
                    data[field] = data[model_aliases[field]]  # type: ignore[index]
                    data.pop(model_aliases[field])  # type: ignore[arg-type]
                    missing_fields.remove(field)

                if hasattr(model_types[field], "__args__") and NoneType in model_types[field].__args__:  # type: ignore[union-attr] # noqa: SIM102
                    if field in missing_fields:
                        # If the field is optional and it is not provided, set it to None
                        provided_fields.add(field)
                        data[field] = None  # type: ignore[assignment]
                        missing_fields.remove(field)

                if field in model_defaults:
                    # If the field has a default value and it is not provided, set it to the default value
                    if field in data:
                        continue

                    if field in missing_fields:
                        provided_fields.add(field)
                        data[field] = model_defaults[field]
                        missing_fields.remove(field)

        if missing_fields:
            raise MissingFieldsError(missing_fields=missing_fields)

        extra_fields = provided_fields - model_fields
        if extra_fields:
            raise ExtraFieldsError(extra_fields=extra_fields)

        model = self.__class__.model_construct(_fields_set=provided_fields, **data)
        self.__dict__.update(model.__dict__)
