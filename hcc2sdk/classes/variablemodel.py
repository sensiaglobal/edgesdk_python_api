#
# Mario Torre - 12/19/2023
#
   
from enum import Enum

class quality_enum (Enum):
    OK = 0,
    OLD = 1,
    BAD = 2,
    UNKNOWN = -1

    @staticmethod
    def convert_quality_to_string(quality):
        if quality == quality_enum.OK:
            return "OK"
        if quality == quality_enum.OLD:
            return "OLD"
        if quality == quality_enum.BAD:
            return "BAD"
        return "UNKNOWN"

    @staticmethod
    def convert_string_to_quality(str):
            if str.upper() == "OK":
                return quality_enum.OK
            if str.upper() ==  "OLD":
                return quality_enum.OLD
            if str.upper() == "BAD":
                return quality_enum.BAD
            return quality_enum.UNKNOWN

class variable_model:
    def __init__(self, vrm):
        self.name = vrm.name
        self.type = vrm.type
        self.collection_size = vrm.collection_size
        self.register_type = vrm.register_type
        self.register_number = vrm.register_number
        self.num_registers = vrm.num_registers
        self.writable = vrm.writable
        self.word_swap = vrm.word_swap
        self.byte_swap = vrm.byte_swap
        self.realtime_data = realtime_data()
        self.realtime_control = realtime_control()
    
class realtime_data:

    def __init__(self, value=None, dtype=None, quality=quality_enum.UNKNOWN, timestamp=None):
        self.value = value
        self.dtype = dtype
        self.quality = quality
        self.timestamp = timestamp

    def __str__(self):
        return f'v: {self.value}, ty {self.dtype}, q: {self.quality}, ts: {self.timestamp}'

        
class realtime_control (realtime_data):

    def __init__(self, value=None, dtype=None, quality=quality_enum.UNKNOWN, timestamp=None, control_pending=False):
        super().__init__(value, dtype, quality, timestamp)
        self.control_pending = control_pending

    def __str__(self):
        return f'v: {self.value}, ty: {self.dtype}, q: {self.quality}, ts: {self.timestamp}, pending: {self.control_pending} '
