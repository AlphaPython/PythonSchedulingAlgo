class Process(object):
    def __init__(self):
        self.process_name = ""
        self.arrival_time = 0
        self.bust_time = 0
        self.start_time = 0
        self.end_time = 0
        self.start_set = False
        self.io_bust = 0
        self.io_interrupt_time = -1
        self.io_int_count = 0
        self.done_time_slice = 0
        self._added = True
        self._bust = 0
