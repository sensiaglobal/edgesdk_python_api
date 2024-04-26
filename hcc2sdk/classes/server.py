#
# Mario Torre - 12/19/2023
#
class Server:
    def __init__(self, host, port, unit, time_period, control_time_period, timeout, retries):
        self.host = host
        self.port = port
        self.unit = unit
        self.time_period = time_period
        self.control_time_period = control_time_period
        self.timeout = timeout
        self.retries = retries
        
