#
# Mario Torre - 12/19/2023
#
from threading import Thread
import time
from hcc2sdk.classes.datatype import data_type, data_type_enum
from hcc2sdk.classes.variablemodel import quality_enum
from hcc2sdk.classes.scanbucket import scan_bucket
from hcc2sdk.const.contants import MINANALOGBUCKETSIZE, MINDIGITALBUCKETSIZE
from hcc2sdk.lib.miscfuncs import bin_to_double, convert_unsigned_to_signed, double_to_bin, bin_to_float, float_to_bin, merge_int_16_to_32, setup_parameter, split_int_16, split_int_16_double, swap_word_bytes, swap_word_bytes_double
from hcc2sdk.classes.registertype import register_type, register_type_enum, register_vars
from hcc2sdk.lib.modbuslib import modbus_lib
from pymodbus.client.tcp import ModbusTcpClient
# -----------------------------------------------------------------------------
#
# Main entry 
#
# ------------------------------------------------------------------------------
def modbus_engine(logger, config, server, vars, db, event):
      
    logger.info ("Modbus client engine started")
    #
    # define arrays and lists
    #
    vars_list = []
    buckets_dict = dict()
    #
    # A bucket is a set of consecutive registers (of a specific register type) within the bucket size.
    # Get the bucket sizes.
    #
    digital_bucket_size = config.engine.digital_bucket_size
    digital_bucket_size = setup_parameter(digital_bucket_size, MINDIGITALBUCKETSIZE)
    analog_bucket_size = config.engine.analog_bucket_size
    analog_bucket_size = setup_parameter(analog_bucket_size, MINANALOGBUCKETSIZE)
    prev_status = False
    scan_ratio = int(server.time_period/server.control_time_period)
    #
    # Arrange the variables that are needed to scan (or write)
    #
    vars_list.append(register_vars(register_type_enum.INPUT_STATUS, vars.Variables.Input_status))
    vars_list.append(register_vars(register_type_enum.COIL, vars.Variables.Coils))
    vars_list.append(register_vars(register_type_enum.INPUT_REGISTER, vars.Variables.Input_registers))
    vars_list.append(register_vars(register_type_enum.HOLDING_REGISTER, vars.Variables.Holding_registers))
    #
    # create the buckets on each case
    #
    try:
        for vml in vars_list:
            bucket_size = digital_bucket_size
            if (vml.type == register_type_enum.INPUT_REGISTER) or (vml.type == register_type_enum.HOLDING_REGISTER):
                bucket_size = analog_bucket_size
            bucket_list = scan_bucket.define_scan_buckets(vml.vars, bucket_size)
            db.add_variable_list_to_DB(vml)
            buckets_dict[vml.type] = bucket_list
    except Exception as e:
        logger.error("Unable to create the buckets. Error: " + str(e) + ". Application Aborted.")
        return
    #
    # Try to connect with server
    #
    client = ModbusTcpClient(host=server.host, port=server.port, timeout=float(server.timeout/1000), close_comm_on_error=True, retries=server.retries)
    mbl = modbus_lib(client)

    ok = False

    while (ok == False):
        
        try:
            ok = mbl.client.connect()
        except Exception as e:
            logger.warning("Unable to connect with modbus server. Error: " + str(e) + ". Retrying...")
        finally:
            time.sleep(server.control_time_period / 1000)

    logger.info ("Connection with host: " + server.host + ", port: " + str(server.port) + " established ok.") 
    #
    # Connection is ok. Start scanning according to buckets
    #
    ratio_counter = 0
    while (ok):

        #
        # Scan to all buckets completed
        # let's check if there are any pending commands to issue
        #
        comm_status = True

        try:
            logger.debug(">> Issuing controls.... ")
            issue_pending_controls(logger, db, mbl, server)
        except Exception as e:
            logger.error("Error trying to issue commands to server: " + server.host + ", Port: " + str(server.port) + ". Error: " + str(e) + ". Retrying...")
            comm_status = False

        if ratio_counter == 0:
            for key, buckets in buckets_dict.items():
            
                scan_method = ""
                comm_status = True
                try:
                    for bucket in buckets:
                        if (key == register_type_enum.INPUT_STATUS):
                                scan_method = "scan_input_status"
                                logger.debug(">> Scanning: " + scan_method)
                                scan_input_status(logger, db, mbl, server, bucket)
                                continue
                        if (key == register_type_enum.COIL):
                                scan_method = "scan_coil"
                                logger.debug(">> Scanning: " + scan_method)
                                scan_coil(logger, db, mbl, server, bucket)
                                continue
                        if (key == register_type_enum.INPUT_REGISTER):
                                scan_method = "scan_input_register"
                                logger.debug(">> Scanning: " + scan_method)
                                scan_input_register(logger, db, mbl, server, bucket)
                                continue
                        if (key == register_type_enum.HOLDING_REGISTER):
                                scan_method = "scan_holding_register"
                                logger.debug(">> Scanning: " + scan_method)
                                scan_holding_register(logger, db, mbl, server, bucket)
                                continue
                        else:
                            logger.error("Type of register is not allowed. Please check configuration.")
                            comm_status = False
                            break
                except Exception as e:
                    logger.error("Unable to process data from host: " + server.host + ", Port: " + str(server.port) + ", Method: " + scan_method + ". Error: " + str(e));
                    #
                    # comms failed. let's wait a while and try again
                    #
                    comm_status = False
                    time.sleep(server.control_time_period / 1000)
                    #
                    # try to reconnect
                    #
                    if client.connected == False:
                        mbl.client.close()
                        mbl.client.connect()
                        logger.info ("Closing prev connection an re-connect with host: " + server.host + ", port: " + str(server.port) + " established ok.") 
                        time.sleep(2 * server.control_time_period / 1000)
                    continue
            #
            # if scans were successful, fire up the app
            #
            if comm_status == True:
                #
                # fire up apps
                #
                event.set()
        #
        # if communication failed for some reason, put the quality of all data in OLD
        #
        if not comm_status and prev_status:
            db.set_all_quality(quality_enum.OLD)
        
        prev_status = comm_status
        #
        # Follow the scan/control ratio
        #
        ratio_counter += 1
        if ratio_counter == scan_ratio:
            ratio_counter = 0
        #
        # Sleep between pools
        #
        time.sleep(server.control_time_period / 1000)


# -----------------------------------------------------------------------------
#
# Scan methods 
#
# ------------------------------------------------------------------------------
def scan_input_status(logger, db, mbl, server, bucket):
    scan_digital(logger, db, mbl, server, bucket, register_type_enum.INPUT_STATUS)

def scan_coil(logger, db, mbl, server, bucket):
    scan_digital(logger, db, mbl, server, bucket, register_type_enum.COIL)

def scan_input_register(logger, db, mbl, server, bucket):
    scan_analog_register(logger, db, mbl, server, bucket, register_type_enum.INPUT_REGISTER)

def scan_holding_register(logger, db, mbl, server, bucket):
    scan_analog_register(logger, db, mbl, server, bucket, register_type_enum.HOLDING_REGISTER)

def scan_digital(logger, db, mbl, server, bucket, reg_type):

    #while count > 0:
    try:
        if (reg_type == register_type_enum.INPUT_STATUS):
            #
            # scan. If comm failure it will return Modbus.SlaveException
            #
            data = mbl.read_input_status(server.unit, bucket.start_register, bucket.num_registers).bits
        else:
            data = mbl.read_coils(server.unit, bucket.start_register, bucket.num_registers).bits
        #
        # try to place each register to its corresponding place in DB
        #
    except Exception as e:
        raise Exception("Exception (digital) - " + str(e) + " unable to acquire data")
      
    for tag_name in bucket.tag_names:
        
        vrm =  db.get_variables_model_from_DB(tag_name)

        if vrm is None:
            raise Exception("tagname: " + tag_name + " does not exist yet in DB.")
        
        for i in range(vrm.register_number, vrm.register_number + vrm.num_registers):
            bvalue = data[i - bucket.start_register]
        #
        # save to DB
        #
        if (db.update_realtime_data_on_DB(tag_name, bvalue, data_type.convert_string_to_type(vrm.type), quality_enum.OK) == False):
            raise Exception("tagname: " + tag_name + " does not exist yet in DB.")
         
    return

def scan_analog_register(logger, db, mbl, server, bucket, reg_type):

    try:
        if (reg_type == register_type_enum.INPUT_REGISTER):
            #
            # Scan Input Registers. If comm failure it will return Exception
            #
            data = mbl.read_input_registers(server.unit, bucket.start_register, bucket.num_registers).registers

        elif (reg_type == register_type_enum.HOLDING_REGISTER):
            #
            # Scan Holding registers. If comm failure it will return Exception
            #
            data = mbl.read_holding_registers(server.unit, bucket.start_register, bucket.num_registers).registers
        else:
            raise Exception("Invalid register type on call. Review configuration.")
        
    except Exception as e:
        raise Exception("Exception (analog) - " + str(e) + " unable to acquire data") 

    # 
    # check if we received the correct number of registers
    #
    if len(data) != bucket.num_registers:
        raise Exception("Error (analog) Number of received items (" + str(len(data)) + ") is different from number of requested items (" + str(bucket.num_registers)+")")
    #
    # try to place each register to its corresponding place in DB
    #
    for tag_name in bucket.tag_names:
        ivalue = 0
        fvalue = 0.0

        vrm =  db.get_variables_model_from_DB(tag_name)
        if vrm is None: 
            raise Exception("tagname: " + tag_name + " does not exist yet in DB.")

        value_array = []
        for element in range(vrm.collection_size):        
            
            j = 0
            ivalue = 0
            initial_register = vrm.register_number + (element * vrm.num_registers)

            for i in range(initial_register, initial_register + vrm.num_registers):

                if vrm.word_swap == False:
                    ivalue = (ivalue << 16) + data[i - bucket.start_register]
                else:                
                    ivalue = (data[i - bucket.start_register]<< (16*j)) + ivalue
                j+=1
            #
            # convert to the appropriate type
            #
            dtype = data_type.convert_string_to_type(vrm.type)
            if dtype == data_type_enum.TYPE_FLOAT:
                #
                # Convert integer to float
                #
                fvalue = bin_to_float(ivalue)
                #
                # save to DB
                #
                ovalue = fvalue
            elif dtype == data_type_enum.TYPE_DOUBLE:
                #
                # Convert integer to double
                #
                fvalue = bin_to_double(ivalue)
                #
                # save to DB
                #
                ovalue = fvalue
            else:
                ovalue = convert_unsigned_to_signed (ivalue, vrm.num_registers)
                
            value_array.append(ovalue)

        if len (value_array) == 1:
            if db.update_realtime_data_on_DB(tag_name, value_array[0], dtype, quality_enum.OK) == False:
                raise Exception("tagname: " + tag_name + " does not exist yet in DB.")
        else:
            if db.update_realtime_data_on_DB(tag_name, value_array, dtype, quality_enum.OK) == False:
                raise Exception("tagname: " + tag_name + " does not exist yet in DB.")


    return

# -----------------------------------------------------------------------------
#
# Control Methods
#
# ------------------------------------------------------------------------------
def issue_pending_controls(logger, db, mbl, server):
    #
    # go through db so check if there are any pending controls
    #
    vml = db.get_pending_control_from_queue()
    #
    # issue those controls
    #
    for vm in vml:
        rtype = register_type.convert_string_to_register_type(vm.register_type)
        dtype = data_type.convert_string_to_type(vm.type)
        value = vm.realtime_control.value
        #
        # check register type
        #
        if rtype == register_type_enum.COIL:
            # issue the coil control  
            mbl.write_coils(server.unit, vm.register_number, value)

        elif rtype == register_type_enum.HOLDING_REGISTER:
            #
            # only scalars allowed to be written back
            #
            if vm.collection_size == 1:
                # issue control depending of number of registers
                if vm.num_registers == 1:
                    if dtype == data_type_enum.TYPE_FLOAT:
                        logger.error ("Tag: " + vm.name + " - Invalid data type. Number of registers: " + str(vm.num_registers) + " is not allowed for a double. Write skipped.")
                        continue
                    
                    elif dtype == data_type_enum.TYPE_DOUBLE:
                        logger.error ("Tag: " + vm.name + " - Invalid data type. Number of registers: " + str(vm.num_registers) + " is not allowed for a float. Write skipped.")
                        continue

                    elif dtype == data_type_enum.TYPE_INTEGER:
                        ivalue  = value & 0xFFFF
                    else:
                        ivalue = value
                    try:
                        mbl.write_holding_register(server.unit, vm.register_number, ivalue)
                    except Exception as e:
                        logger.error ("Tag: " + vm.name + " - Error trying to write on unit: " + str(server.unit) + ", reg number: " + str(vm.register_number) + ", value: " + str(ivalue) + ". Error: " + str(e) + ". Write skipped.")
                        continue

                elif vm.num_registers == 2:
                    ivalue = 0
                    if dtype == data_type_enum.TYPE_DOUBLE:
                        logger.error ("Tag: " + vm.name + " - Invalid data type. Number of registers: " + str(vm.num_registers) + " is not allowed for a double. Write skipped.")
                        continue
                    elif dtype == data_type_enum.TYPE_FLOAT:
                        ivalue = float_to_bin(value)
                    elif dtype == data_type_enum.TYPE_INTEGER:
                        ivalue = value & 0xFFFFFFFF
                    else: 
                        ivalue = value
                    try:
                        ivalue = swap_word_bytes(ivalue, vm.word_swap, vm.byte_swap)
                        mbl.write_holding_register32(server.unit, vm.register_number, split_int_16(ivalue))
                    except Exception as e:
                        logger.error ("Tag: " + vm.name + " - Error trying to write on unit: " + str(server.unit) + ", reg number: " + str(vm.register_number) + ", value: " + str(ivalue) + ", Error: " + str(e) + ". Write skipped.")
                        continue

                elif vm.num_registers == 4:
                    ivalue = 0
                    if dtype == data_type_enum.TYPE_DOUBLE:
                        ivalue = double_to_bin(value)
                    elif dtype == data_type_enum.TYPE_FLOAT:
                        logger.error ("Tag: " + vm.name + " - Invalid data type. Number of registers: " + str(vm.num_registers) + " is not allowed for a float. Write skipped.")
                        continue
                    elif dtype ==data_type_enum.TYPE_INTEGER:
                        ivalue = value & 0xFFFFFFFFFFFFFFFF
                    else: 
                        ivalue = value
                    try:
                        ivalue = swap_word_bytes_double(ivalue, vm.word_swap, vm.byte_swap)
                        mbl.write_holding_register32(server.unit, vm.register_number, split_int_16_double(ivalue))
                    except Exception as e:
                        logger.error ("Tag: " + vm.name + " - Error trying to write on unit: " + str(server.unit) + ", reg number: " + str(vm.register_number) + ", value: " + str(ivalue) + ", Error: " + str(e) + ". Write skipped.")
                        continue
                else:
                    logger.error ("Tag: " + vm.name + " - Invalid register type. Number of registers: " + str(vm.num_registers) + " is not allowed. Write skipped")
                    continue
            else:
                logger.error ("Tag: " + vm.name + " - Is an array. Writing with arrays is not allowed. Write skipped.")
                continue
        else: 
            logger.error ("Tag: " + vm.name + " - Invalid register type. Register type: " + str(vm.register_type) + " cannot be written. Write skipped.")
        #
        # update database
        #
        db.clear_update_bit_control_on_DB(vm.name)
