def get_bfs_level(gnodes):

    tag_visited = [0 for i in range(len(gnodes))]
    bfs_result = [-1 for i in range(len(gnodes))]
    temp_count = 0
    while 0 in tag_visited:
        temp_count += 1
        for idx in range(len(gnodes)):
            pre_ok = True

            if len(gnodes[idx].src) == 0:
                tag_visited[idx] = 1
                bfs_result[idx] = 0
                continue

            for pre_id in gnodes[idx].src:
                if tag_visited[pre_id] == 0:
                    pre_ok = False
                    break

            if pre_ok:
                max_pre_stage = bfs_result[gnodes[idx].src[0]]
                for pre_id in gnodes[idx].src:
                    if max_pre_stage < bfs_result[pre_id]:
                        max_pre_stage = bfs_result[pre_id]
                tag_visited[idx] = 1
                bfs_result[idx] = max_pre_stage + 1
            # print(bfs_result)
    return bfs_result

# def get_bfs_level(dependency):
#     """ input
#     dependency: the dependency of each op in the dag. list of list
#     """
#     length = len(dependency)
#     tag_visited = [0 for i in range(length)]
#     bfs_result = [-1 for i in range(length)]
#     """for i in range(length):
#         if dependency[i] == [-2]:
#             bfs_result[i] = -20
#             tag_visited[i] = 1"""
#     temp_count = 0
#     while 0 in tag_visited:
#         temp_count += 1
#         for idx in range(length):
#             pre_ok = True

#             if dependency[idx][0] == -3:
#                 bfs_result[idx] = 0
#                 tag_visited[idx] = 1
#                 continue # Const, initial ready

#             if dependency[idx][0] == -1:
#                 tag_visited[idx] = 1
#                 bfs_result[idx] = 0
#                 continue

#             for pre_id in dependency[idx]:
#                 if tag_visited[pre_id] == 0:
#                     pre_ok = False
#                     break

#             if pre_ok:
#                 max_pre_stage = bfs_result[dependency[idx][0]]
#                 for pre_id in dependency[idx]:
#                     if max_pre_stage < bfs_result[pre_id]:
#                         max_pre_stage = bfs_result[pre_id]
#                 tag_visited[idx] = 1
#                 bfs_result[idx] = max_pre_stage + 1
#             # print(bfs_result)
#     return bfs_result


# def combine_bfs_bias_to_schedule(bfs, bias, dependency):
#     length = len(dependency)
#     ops_stage = [0 for i in range(length)]
#     tag_visited = [0 for i in range(length)]
    
#     while 0 in tag_visited:
#         for idx in range(length):
#             pre_ok = True
#             if dependency[idx][0] == -3:
#                 ops_stage[idx] = 0 # 好像没必要+bias
#                 tag_visited[idx] = 1
#                 continue # Const, initial ready
            
#             if dependency[idx][0] == -1:
#                 ops_stage[idx] = bias[idx]
#                 tag_visited[idx] = 1
#                 continue
            
#             for pre_id in dependency[idx]:
#                 if tag_visited[pre_id] == 0:
#                     pre_ok = False
#                     break
            
#             if pre_ok:
#                 max_pre_stage = ops_stage[dependency[idx][0]]
#                 for pre_id in dependency[idx]:
#                     if max_pre_stage < ops_stage[pre_id]:
#                         max_pre_stage = ops_stage[pre_id]
#                 if (max_pre_stage + 1) > (bfs[idx] + bias[idx]):
#                     ops_stage[idx] = max_pre_stage + 1
#                 else:
#                     ops_stage[idx] = (bfs[idx] + bias[idx])
#                 tag_visited[idx] = 1
#     stage_schedule = [[] for i in range(max(ops_stage) + 1)]
#     for idx in range(length):
#         stage_schedule[ops_stage[idx]].append(idx)
#     return ops_stage, stage_schedule


def combine_bfs_bias_to_schedule(schedule, bias, gnodes):
    ops_stage = [0 for i in range(len(gnodes))]
    tag_visited = [0 for i in range(len(gnodes))]
    
    while 0 in tag_visited:
        for idx in range(len(gnodes)):
            pre_ok = True
            if len(gnodes[idx].src == 0):
                ops_stage[idx] = 0
                tag_visited[idx] = 1
                continue # Const, initial ready
            
            for pre_id in gnodes[idx].src:
                if tag_visited[pre_id] == 0:
                    pre_ok = False
                    break
            
            if pre_ok:
                max_pre_stage = ops_stage[gnodes[idx].src[0]]
                for pre_id in gnodes[idx].src:
                    if max_pre_stage < ops_stage[pre_id]:
                        max_pre_stage = ops_stage[pre_id]
                if (max_pre_stage + 1) > (schedule[idx] + bias[idx]):
                    ops_stage[idx] = max_pre_stage + 1
                else:
                    ops_stage[idx] = (schedule[idx] + bias[idx])
                tag_visited[idx] = 1
    stage_schedule = [[] for i in range(max(ops_stage) + 1)]
    for idx in range(len(gnodes)):
        stage_schedule[ops_stage[idx]].append(idx)
    return ops_stage, stage_schedule