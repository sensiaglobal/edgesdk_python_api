#
# Mario Torre - 12/19/2023
#
from enum import Enum

class register_vars:
    def __init__(self, type, vars):
        self.type = type
        self.vars = vars


class register_type_enum(Enum):
    UNKNOWN = 0
    INPUT_STATUS = 1
    COIL = 2
    INPUT_REGISTER = 3
    HOLDING_REGISTER = 4

class register_type:

    INPUTSTATUS = "input_status"
    COIL = "coil"
    INPUTREGISTER = "input_register"
    HOLDINGREGISTER = "holding_register"
    UNKNOWN = "unknown"

    registerMap = dict() 
    registerMap[INPUTSTATUS] = register_type_enum.INPUT_STATUS
    registerMap[COIL] = register_type_enum.COIL
    registerMap[INPUTREGISTER] = register_type_enum.INPUT_REGISTER
    registerMap[HOLDINGREGISTER] = register_type_enum.HOLDING_REGISTER
    registerMap[UNKNOWN] = register_type_enum.UNKNOWN 

    @classmethod
    def convert_string_to_register_type(cls, type):
            return cls.registerMap[type]
    
    @classmethod
    def convert_register_type_to_string(cls, reg):
        if (reg == register_type_enum.INPUT_STATUS):
            return cls.INPUTSTATUS
        if (reg == register_type_enum.COIL):
            return cls.COIL
        if (reg == register_type_enum.INPUT_REGISTER):
                return cls.INPUTREGISTER
        if (reg == register_type_enum.HOLDING_REGISTER):
                return cls.HOLDINGREGISTER
        return cls.UNKNOWN   
    