#
# Mario Torre - 12/19/2023
#
from enum import Enum

class data_type_enum (Enum):
        TYPE_BOOLEAN = 1,
        TYPE_INTEGER = 2,
        TYPE_UNSIGNED = 3,
        TYPE_FLOAT = 4,
        TYPE_DOUBLE = 5,
        TYPE_UNKNOWN = 0

class data_type:
        TYPE_BOOLEAN = "boolean"
        TYPE_INTEGER = "integer"
        TYPE_UNSIGNED = "unsigned"
        TYPE_FLOAT = "float"
        TYPE_DOUBLE = "double"
        TYPE_UNKNOWN = "unknown"
        type_map = dict()
    
        type_map[TYPE_BOOLEAN] = data_type_enum.TYPE_BOOLEAN
        type_map[TYPE_INTEGER] = data_type_enum.TYPE_INTEGER
        type_map[TYPE_UNSIGNED] = data_type_enum.TYPE_UNSIGNED
        type_map[TYPE_FLOAT] = data_type_enum.TYPE_FLOAT
        type_map[TYPE_DOUBLE] = data_type_enum.TYPE_DOUBLE
        type_map[TYPE_UNKNOWN] = data_type_enum.TYPE_UNKNOWN
 
        @classmethod
        def convert_string_to_type(cls, data_type):
            return cls.type_map[data_type]

        @classmethod
        def convert_type_to_string(cls, reg):
            if reg == data_type_enum.TYPE_BOOLEAN:
                return cls.TYPE_BOOLEAN
            if reg == data_type_enum.TYPE_INTEGER:
                return cls.TYPE_INTEGER
            if reg == data_type_enum.TYPE_UNSIGNED:
                return cls.TYPE_UNSIGNED
            if reg == data_type_enum.TYPE_FLOAT:
                return cls.TYPE_FLOAT
            if reg == data_type_enum.TYPE_DOUBLE:
                return cls.TYPE_DOUBLE
            return cls.TYPE_UNKNOWN
        
        @classmethod
        def convert_string_to_type(cls, str):
            return data_type.type_map[str]

        @classmethod
        def convert_raw_value_to_appropiate_type(cls, dtype, raw_value):
            if dtype == data_type_enum.TYPE_BOOLEAN:
                value = bool(raw_value)
            elif dtype == data_type_enum.TYPE_INTEGER:
                value = int(raw_value)
            elif dtype == data_type_enum.TYPE_UNSIGNED:
                value = int(raw_value) 
            elif dtype == data_type_enum.TYPE_FLOAT:
                value = float(raw_value)
            elif dtype == data_type_enum.TYPE_DOUBLE:
                value = float(raw_value)
            else:
                value = raw_value
            return value
