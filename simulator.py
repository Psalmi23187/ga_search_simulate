# author: yhc
import json
import numpy as np
from random import shuffle

class Simulator:
    def __init__(self, layer_schedule, pe_num, gnodes):
        self.layer_schedule = layer_schedule
        self.pe_num = pe_num
        self.gnodes = gnodes

        self.sm_info = {}
        for i in range(self.pe_num):
            self.sm_info[i] = {
                "sm_id": i,
                "last_used_time": 0,
                "status": "unused"
            }

        self.op_info = {}
        for idx in range(len(self.gnodes)):
            self.op_info[idx] = {
                "operator_id": idx,
                "begin_time": -1,
                'sm_used': 0,
                "latency": gnodes[idx].latency,
                "status": "unexecuted"
            }
        self.unused_pe_num = self.pe_num
        self.total_latency = 0
        self.temp_layer = 0

    def step_sm_allocate(self):
        # min-max method
        self.unused_pe_num = self.pe_num
        self.temp_layer += 1
        # print(self.layer_schedule)
        if self.temp_layer >= len(self.layer_schedule):
            return
        current_step_schedule_list = self.layer_schedule[self.temp_layer]

        if len(current_step_schedule_list) == 0:
            return
        if self.pe_num < len(current_step_schedule_list):
            print(self.temp_layer)
            # for idx in current_step_schedule_list:
            #     self.gnodes[idx].print_info()
            print("warning, pe_num too few, could not support entirely parallel!")
            return

        for idx in current_step_schedule_list:
            #if op_id_to_type(idx) not in [-2,-3]:
            self.op_info[idx]["sm_used"] = 1
            self.unused_pe_num -= 1
        
        while(self.unused_pe_num >= 1):
            kernel_latencys = [self.gnodes[idx].estimate_latency(self.op_info[idx]["sm_used"]) \
                                                            for idx in current_step_schedule_list]
            max_latency = max(kernel_latencys)
            max_latency_idx = kernel_latencys.index(max_latency)

            if self.op_info[max_latency_idx]["sm_used"] >= 80:
                break
            else:
                self.op_info[max_latency_idx]["sm_used"] += 1
                self.unused_pe_num -= 1
        
        for idx in current_step_schedule_list:
            pass

        self.total_latency += max([self.gnodes[idx].estimate_latency(self.op_info[idx]["sm_used"]) \
                                                            for idx in current_step_schedule_list])

def layer_schedule_to_latency(layer_schedule, gnodes):
    pe_num = 80
    simulator = Simulator(layer_schedule, pe_num, gnodes)
    for i in range(len(layer_schedule)):
        simulator.step_sm_allocate()
    return simulator.total_latency
