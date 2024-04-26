#
# Merio Torre - 03/28/2024
#
class MyConfig (object):
    def __init__(self):
        self.version = "0.1.0"
        self.variable_file = "appconfig/vars.json"
        self.app = App()
        self.opts = Opts()
        self.env = Env()
        self.engine = Engine()
        self.lod = log()

class App (object):
    def __init__(self):
        self.server_default_host = "localhost"
        self.server_default_port = 502
        self.server_default_unit = 1
        self.default_time_period = 1000
        self.default_control_time_period = 1000
        self.default_timeout = 500
        self.default_retries = 0

class Opts(object):
    def __init__(self):
        self.host_help = "Modbus server hoSt"
        self.port_help = "Modbus server Port"
        self.unit_help = "Unit (Slave ID)"
        self.time_period_help = "data update Time period"
        self.control_time_period_help ="control update Time period"
        self.timeout_help = "client timeoUt"
        self.retries_help = "client retries"
        self.version_help = "current version"

class Env (object):
    def __init__(self):
        self.modbus_host = "HOST"
        self.modbus_port = "PORT"
        self.modbus_unit = "UNIT"
        self.time_period = "TIME_PERIOD"
        self.control_time_period = "CONTROL_TIME_PERIOD"
        self.timeout = "TIMEOUT"
        self.retries = "RETRIES"        

class Engine (object):
    def __init__(self):
        self.analog_bucket_size = 10
        self.digital_bucket_size = 16

class log (object):
    def __init__(self):
        self.log_to_file = False
        self.log_file = "logs/modbus-engine.log"
        self.level = "INFO"
        self.format = "[0][%(asctime)s.%(msecs)03dZ][%(name)s][%(levelname)s]%(message)s"
        self.date_format = "%Y-%m-%dT%H:%M:%S"
    