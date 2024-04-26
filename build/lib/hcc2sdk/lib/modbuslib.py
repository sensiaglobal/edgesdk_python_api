#
# Mario Torre - 12/19/2023
#
class modbus_lib:

    def __init__(self, client):
        self.client = client

    def read_input_registers(self, unit, start_address, num_inputs):
        return self.client.read_input_registers(start_address, num_inputs, unit)
    
    def read_holding_registers(self, unit, start_address, num_inputs):
        return self.client.read_holding_registers(start_address, num_inputs, unit)
    
    def read_input_status(self, unit, start_address, num_inputs):
        return self.client.read_discrete_inputs(start_address, num_inputs, unit)
    
    def read_coils(self, unit, start_address, num_inputs):
        return self.client.read_coils(start_address, num_inputs, unit)
    
    def write_coils(self, unit, start_address, value):
        self.client.write_coil(start_address, value, unit)

    def write_holding_register(self, unit, start_address, value):
        self.client.write_register(start_address, value, unit)
    
    def write_holding_register32(self, unit, start_address, value_array):
        self.client.write_registers(start_address, value_array, unit)
