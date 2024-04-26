#
# Mario Torre - 12/19/2023
#
from datetime import datetime
from queue import Empty
from hcc2sdk.classes.registertype import register_type
from hcc2sdk.classes.variablemodel import realtime_control, realtime_data, variable_model

class DB:
    def __init__(self, control_queue, db_mutex):
        self.matrix = dict()
        self.control_queue = control_queue
        self.db_mutex = db_mutex

    def add_variable_list_to_DB(self, dictionary):
        for vrm in dictionary.vars:
            vrm.register_type = register_type.convert_register_type_to_string(dictionary.type)
            with self.db_mutex:
                self.matrix[vrm.name] = variable_model(vrm)

    def get_variables_model_from_DB(self, tag_name):
        rtn = None
        with self.db_mutex:
            if tag_name in self.matrix:
                rtn = self.matrix[tag_name]
        return rtn

    def update_realtime_data_on_DB(self, tag_name, value, type, quality):
        rtn = False
        with self.db_mutex:
            if tag_name in self.matrix:
                self.matrix[tag_name].realtime_data = realtime_data(value, type, quality, datetime.utcnow())
                rtn = True
        return rtn
    
    def update_realtime_control_on_DB(self, tag_name, value, type, quality):
        rtn = False
        with self.db_mutex:
            if tag_name in self.matrix:
                self.matrix[tag_name].realtime_control = realtime_control(value, type, quality, datetime.utcnow(), True)
                rtn = True
        return rtn

    def update_realtime_control_queue_on_DB(self, tag_name, value, type, quality):
        rtn = False
        if tag_name in self.matrix:
            self.matrix[tag_name].realtime_control = realtime_control(value, type, quality, datetime.utcnow(), True)
            self.control_queue.put({"tag_name": tag_name, "control": self.matrix[tag_name].realtime_control})
            rtn = True
        return rtn


    def get_all_pending_control_vars(self): 
        rtn = []
        with self.db_mutex:
            for  key, vml in self.matrix.items():
                if vml is not None:
                    if vml.writable == True:
                        if vml.realtime_control.control_pending == True:
                            rtn.append(vml)
        return rtn
    
    def get_pending_control_from_queue(self):
        rtn = []
        controls = [] 
        with self.db_mutex:
            while True:
                try:
                    controls.append(self.control_queue.get(block=False))
                except Empty as e:
                    break
            if len(controls) > 0:
                self.control_queue.task_done()
                for control in controls:
                    vml = self.matrix[control['tag_name']]
                    vml.realtime_control = control["control"]                
                    rtn.append(vml)
        return rtn

    def set_all_quality(self, quality):

        with self.db_mutex:
            for name, vml in self.matrix.items():
                vml.realtime_data.quality = quality

    def get_value(self, tag_name):
        rtn = None
        with self.db_mutex:
            if tag_name in self.matrix:
                rtn = self.matrix[tag_name].realtime_data
            return rtn


    def set_value(self, tag_name, value, quality):
        rtn = False
        with self.db_mutex:
            if tag_name in self.matrix:
                dtype = self.matrix[tag_name].realtime_data.dtype
                writable = self.matrix[tag_name].writable
                if writable == True:
                    self.update_realtime_control_queue_on_DB(tag_name, value, dtype, quality)
                    rtn = True
        return rtn
    
    def clear_update_bit_control_on_DB(self, tag_name):

        rtn = False
        with self.db_mutex:
            if tag_name in self.matrix:
                self.matrix[tag_name].realtime_control.control_pending=False
                self.matrix[tag_name].realtime_control.Timestamp = datetime.utcnow()
                rtn = True
        return rtn

