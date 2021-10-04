from data.sources.settings import DataField

from typing import Any, Callable
import pandas as pd
import builtins


def convert_to_df(data: list[dict[str, Any]], fields: list[DataField]) -> pd.DataFrame:
    fields_definition = {field.name: field.type for field in fields}
    builtin_types_fields = {
        name: _type
        for name, _type in fields_definition.items()
        if _type.__name__ in builtins.__dict__
    }
    custom_types_fields = {
        name: _type
        for name, _type in fields_definition.items()
        if name not in builtin_types_fields
    }

    filtered_data = [
        {k: v for k, v in d.items() if k in fields_definition} for d in data
    ]

    return _create_dataframe(filtered_data, builtin_types_fields, custom_types_fields)


def _create_dataframe(
    filtered_data: list[dict[str, Any]],
    builtin_types_fields: dict[str, Callable],
    custom_types_fields: dict[str, Callable],
) -> pd.DataFrame:
    dataframe = pd.DataFrame(filtered_data)

    for field, _type in builtin_types_fields.items():
        dataframe[field] = dataframe[field].astype(_type)

    for field, _type in custom_types_fields.items():
        dataframe[field] = dataframe[field].apply(_type)

    return dataframe
