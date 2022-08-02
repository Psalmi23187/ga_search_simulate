def get_bfs_level(dependency):
    """ input
    dependency: the dependency of each op in the dag. list of list
    """
    length = len(dependency)
    tag_visited = [0 for i in range(length)]
    bfs_result = [-1 for i in range(length)]
    """for i in range(length):
        if dependency[i] == [-2]:
            bfs_result[i] = -20
            tag_visited[i] = 1"""
    temp_count = 0
    while 0 in tag_visited:
        temp_count += 1
        for op_id in range(length):
            pre_ok = True

            if dependency[op_id][0] == -3:
                bfs_result[op_id] = 0
                tag_visited[op_id] = 1
                continue # Const, initial ready

            if dependency[op_id][0] == -1:
                tag_visited[op_id] = 1
                bfs_result[op_id] = 0
                continue

            for pre_id in dependency[op_id]:
                if tag_visited[pre_id] == 0:
                    pre_ok = False
                    break

            if pre_ok:
                max_pre_stage = bfs_result[dependency[op_id][0]]
                for pre_id in dependency[op_id]:
                    if max_pre_stage < bfs_result[pre_id]:
                        max_pre_stage = bfs_result[pre_id]
                tag_visited[op_id] = 1
                bfs_result[op_id] = max_pre_stage + 1
            # print(bfs_result)
    return bfs_result

def combine_bfs_bias_to_schedule(bfs, bias, dependency):
    length = len(dependency)
    ops_stage = [0 for i in range(length)]
    tag_visited = [0 for i in range(length)]
    
    while 0 in tag_visited:
        for op_id in range(length):
            pre_ok = True
            if dependency[op_id][0] == -3:
                ops_stage[op_id] = 0 # 好像没必要+bias
                tag_visited[op_id] = 1
                continue # Const, initial ready
            
            if dependency[op_id][0] == -1:
                ops_stage[op_id] = bias[op_id]
                tag_visited[op_id] = 1
                continue
            
            for pre_id in dependency[op_id]:
                if tag_visited[pre_id] == 0:
                    pre_ok = False
                    break
            
            if pre_ok:
                max_pre_stage = ops_stage[dependency[op_id][0]]
                for pre_id in dependency[op_id]:
                    if max_pre_stage < ops_stage[pre_id]:
                        max_pre_stage = ops_stage[pre_id]
                if (max_pre_stage + 1) > (bfs[op_id] + bias[op_id]):
                    ops_stage[op_id] = max_pre_stage + 1
                else:
                    ops_stage[op_id] = (bfs[op_id] + bias[op_id])
                tag_visited[op_id] = 1
    stage_schedule = [[] for i in range(max(ops_stage) + 1)]
    for op_id in range(length):
        stage_schedule[ops_stage[op_id]].append(op_id)
    return ops_stage, stage_schedule
