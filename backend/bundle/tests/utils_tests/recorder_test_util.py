from __future__ import annotations

from pprint import pformat
from typing import Mapping, List, Union, Optional, Tuple

from bundle.utils.recorder import Recorder


# noinspection PyProtectedMember
class RecorderVar:
    def _validate(self) -> None:
        assert Recorder._TYPE_HEADER in self.var_mapping
        assert Recorder._REPR_HEADER in self.var_mapping

    def _resolve_repr(self) -> None:
        repr_field = self.var_mapping[Recorder._REPR_HEADER]
        type_field = self.var_mapping[Recorder._TYPE_HEADER]
        if isinstance(repr_field, str) and \
                (type_field in Recorder._SINGULAR_TYPES or type_field == Recorder._OBJECT_TYPE_STRING):
            return
        elif isinstance(repr_field, List):
            new_field = []
            if type_field in Recorder._LINEAR_CONTAINER_TYPES:
                for item in repr_field:
                    new_field.append(RecorderVar(item))
            elif type_field in Recorder._PAIR_CONTAINER_TYPES:
                for item in repr_field:
                    new_field.append(
                        {k: RecorderVar(v) for k, v in item.items()}
                    )
            else:
                raise ValueError
            self.var_mapping[Recorder._REPR_HEADER] = new_field
        elif type_field != Recorder._INIT_TYPE_STRING and type_field != Recorder._REFERENCE_TYPE_STRING:
            raise ValueError

    def _resolve_properties(self) -> None:
        if Recorder._PROPERTY_HEADER in self.var_mapping:
            new_field = []
            property_filed = self.var_mapping[Recorder._PROPERTY_HEADER]
            for item in property_filed:
                new_field.append(
                    {k: RecorderVar(v) for k, v in item.items()}
                )
            self.var_mapping[Recorder._PROPERTY_HEADER] = new_field

    def __init__(self, var_mapping: Mapping, var_name: str = None) -> None:
        self.var_mapping = {
            **var_mapping
        }
        self.var_name = var_name
        self._validate()
        self._resolve_repr()
        self._resolve_properties()

    @property
    def type(self) -> str:
        return self.var_mapping[Recorder._TYPE_HEADER]

    @property
    def repr_field(self) -> Union[str, List]:
        return self.var_mapping[Recorder._REPR_HEADER]

    @property
    def cy_id(self) -> int:
        return self.var_mapping.get(Recorder._ID_HEADER, None)

    @property
    def properties(self) -> Optional[RecorderVar]:
        return self.var_mapping.get(Recorder._PROPERTY_HEADER, None)

    def __eq__(self, other: RecorderVar) -> bool:
        flag = True
        flag &= (
                other.type == self.type and other.repr_field == self.repr_field and
                other.cy_id == self.cy_id and other.properties == self.properties and
                other.var_name == self.var_name
        )
        if not flag:
            print(
                f'{self.var_name}: {pformat(self.var_mapping)}'
            )
            print(
                f'{other.var_name}: {pformat(other.var_mapping)}'
            )
        return flag

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


# noinspection PyProtectedMember
class RecorderResultParser:
    @staticmethod
    def _process_records(records: List[Mapping]) -> Tuple[List[Mapping[str, RecorderVar]], List[List[RecorderVar]]]:
        var_list = []
        accessed_var_list = []

        for record in records:
            temp_var_list = {}
            for var_name, var_v in (
                    record[Recorder._VARIABLE_HEADER] if record[Recorder._VARIABLE_HEADER] is not None else {}
            ).items():
                temp_var_list[var_name] = RecorderVar(var_v)

            var_list.append(temp_var_list)

            temp_accessed_var_list = []
            for item in (record[Recorder._ACCESS_HEADER] if record[Recorder._ACCESS_HEADER] is not None else ()):
                temp_accessed_var_list.append(
                    RecorderVar(item)
                )
            accessed_var_list.append(temp_accessed_var_list)

        return var_list, accessed_var_list

    def __init__(self, records: List[Mapping]) -> None:
        self.var_list, self.accessed_var_list = self._process_records(records=records)
        self._records = records

    def __eq__(self, other: RecorderResultParser) -> bool:
        return self.var_list == other.var_list and self.accessed_var_list == other.accessed_var_list

    def __str__(self) -> str:
        return pformat(self._records)

    def __repr__(self) -> str:
        return self.__str__()
