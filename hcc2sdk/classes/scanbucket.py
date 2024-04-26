#
# Mario Torre - 12/19/2023
#
class scan_bucket:
    def __init__(self, start, size):
        self.start_register = start
        self.num_registers = size
        self.tag_names = []

    def add_tags_to_bucket(self, tag_names):
        for tag_name in tag_names:
            if tag_name not in self.tag_names:
                self.tag_names.append(tag_name)

    @staticmethod
    def define_scan_buckets(list, bucket_size):
        rtn = []
        if (len(list) > 0):
            #
            # Go through the whole list 
            # Determine the distance between var registers
            #
            start = -1
            size = -1
            tag_names = []

            check_duplicates = dict()
            list.sort(key=lambda x: x.register_number)

            for vm in list:
                if vm.name in check_duplicates:
                    raise Exception("duplicate variable name found: " + vm.name )
                check_duplicates[vm.name] = vm.name
                #
                # All checks. Build the buckets
                #
                if start < 0:
                    start = vm.register_number
                    size = vm.num_registers * vm.collection_size
                    tag_names.append(vm.name)
                    continue

                if ((vm.register_number - start) <= bucket_size):
                    size = vm.register_number - start + (vm.num_registers * vm.collection_size)
                    tag_names.append(vm.name)
                else:
                    b = scan_bucket(start, size)
                    b.add_tags_to_bucket(tag_names)

                    rtn.append(b)
                    start = vm.register_number
                    size = vm.num_registers * vm.collection_size
                    tag_names = [ vm.name ]

            bucket = scan_bucket(start, size)
            bucket.add_tags_to_bucket(tag_names)
            rtn.append(bucket)
            #
            # Check all buckets for possible overlaps
            #
            i = 0
            for a in rtn:
                j = 0
                for b in rtn:
                    if i != j:
                        if a == b:
                            raise Exception("Register overlapping was found. Application aborted");
                    j+=1
                i+=1
        return rtn
