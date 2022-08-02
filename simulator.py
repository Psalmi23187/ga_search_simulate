# author: yhc
import json
import numpy as np
from random import shuffle

from model_config_nasnet_imagenet_cell_1 import op_runtime_table, get_op_runtime, op_id_to_type, dependency


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
        self.temp_time = 0
        self.temp_layer = -1

    def step_sm_allocate(self):
        # min-max method
        self.unused_pe_num = self.pe_num
        self.temp_layer += 1
        if self.temp_layer >= len(self.layer_schedule):
            return
        current_step_schedule_list = self.layer_schedule[self.temp_layer]
        
        # only schedule op in cell_0
        for op_id in current_step_schedule_list:
            if dependency[op_id][0] == -3: # Const
                current_step_schedule_list.remove(op_id) # remove Const
                continue
            if op_id_to_type(op_id) == -3: # Reduction cell
                current_step_schedule_list.remove(op_id) # remove reduction op

        if len(current_step_schedule_list) == 0:
            return
        if self.pe_num < len(current_step_schedule_list):
            print("warning, pe_num too few, could not support entirely parallel!")
            return

        for op_id in current_step_schedule_list:
            #if op_id_to_type(op_id) not in [-2,-3]:
            self.op_info[op_id]["sm_used"] = 1
            self.unused_pe_num -= 1
        
        while(self.unused_pe_num >= 1):
            temp_id = current_step_schedule_list[0]
            temp_max_runtime = get_op_runtime(temp_id, self.op_info[temp_id]["sm_used"])
            for op_id in current_step_schedule_list[1:]:
                if self.op_info[op_id]["sm_used"] >= 80:
                    continue
                if temp_max_runtime < get_op_runtime(op_id, self.op_info[op_id]["sm_used"]):
                    temp_id = op_id
                    temp_max_runtime  = get_op_runtime(op_id, self.op_info[op_id]["sm_used"])
            if self.op_info[temp_id]["sm_used"] >= 80:
                break
            else:
                self.op_info[temp_id]["sm_used"] += 1
                self.unused_pe_num -= 1
        
        for op_id in current_step_schedule_list:
            pass

        step_max_runtime = get_op_runtime(current_step_schedule_list[0], self.op_info[current_step_schedule_list[0]]["sm_used"])
        for op_id in current_step_schedule_list[1:]:
            if step_max_runtime < get_op_runtime(op_id, self.op_info[op_id]["sm_used"]):
                step_max_runtime = get_op_runtime(op_id, self.op_info[op_id]["sm_used"])
        #if step_max_runtime  > 0:
        #    print(step_max_runtime)
        #print("layer: ", self.temp_layer, " . layer runtime: ", step_max_runtime)
        self.temp_time += step_max_runtime

def layer_schedule_to_runtime(layer_schedule):
    sm_num = 80
    simulator = Simulator(layer_schedule, sm_num, op_runtime_table)
    for i in range(len(layer_schedule)):
        simulator.step_sm_allocate()
    return simulator.temp_time
