# author: yhc
import json
import numpy as np
from random import shuffle

from model_config import op_runtime_table, get_op_runtime, op_id_to_type


class Simulator:
    def __init__(self, layer_schedule, sm_count, operator_runtime, topology=None):
        self.operator_count = 9
        self.layer_schedule = layer_schedule
        self.sm_count = sm_count
        self.operator_runtime = operator_runtime
        self.topology = topology

        self.sm_info = {}
        for i in range(self.sm_count):
            self.sm_info[i] = {
                "sm_id": i,
                "last_used_time": 0,
                "status": "unused"
            }

        self.operator_info = {}
        for i in range(self.operator_count):
            self.operator_info[i] = {
                "operator_id": i,
                "begin_time": -1,
                'sm_used': 0,
                "runtime": operator_runtime[op_id_to_type(i)],
                #"father_id": self.topology[i],
                "status": "unexecuted"
            }
        self.unused_sm_count = self.sm_count
        self.temp_time = 0
        self.temp_layer = -1

    def step_sm_allocate(self):
        # min-max method
        self.unused_sm_count = self.sm_count
        self.temp_layer += 1
        current_step_schedule_list = self.layer_schedule[self.temp_layer]
        if len(current_step_schedule_list) == 0:
            return
        if self.sm_count < len(current_step_schedule_list):
            print("warning, sm_count too few, could not support entirely parallel!")
            return

        for op_id in current_step_schedule_list:
            self.operator_info[op_id]["sm_used"] = 1
            self.unused_sm_count -= 1
        
        while(self.unused_sm_count >= 1):
            temp_id = current_step_schedule_list[0]
            temp_max_runtime = get_op_runtime(temp_id, self.operator_info[temp_id]["sm_used"])
            for op_id in current_step_schedule_list[1:]:
                if self.operator_info[op_id]["sm_used"] >= 80:
                    continue
                if temp_max_runtime < get_op_runtime(op_id, self.operator_info[op_id]["sm_used"]):
                    temp_id = op_id
                    temp_max_runtime  = get_op_runtime(op_id, self.operator_info[op_id]["sm_used"])
            if self.operator_info[temp_id]["sm_used"] >= 80:
                break
            else:
                self.operator_info[temp_id]["sm_used"] += 1
                self.unused_sm_count -= 1
        
        for op_id in current_step_schedule_list:
            pass

        step_max_runtime = get_op_runtime(current_step_schedule_list[0], self.operator_info[current_step_schedule_list[0]]["sm_used"])
        for op_id in current_step_schedule_list[1:]:
            if step_max_runtime < get_op_runtime(op_id, self.operator_info[op_id]["sm_used"]):
                step_max_runtime = get_op_runtime(op_id, self.operator_info[op_id]["sm_used"])
            
        self.temp_time += step_max_runtime

def layer_schedule_to_runtime(layer_schedule):
    sm_num = 80
    simulator = Simulator(layer_schedule, sm_num, op_runtime_table)
    for i in range(len(layer_schedule)):
        simulator.step_sm_allocate()
    return simulator.temp_time
