def get_op_runtime(op_id, sm_used):
    op_type = op_id_to_type(op_id)
    if sm_used % 10 == 0:
        return op_runtime_table[op_type][sm_used]
    else:
        base = (int)(sm_used/10)+1
        return base*10*op_runtime_table[op_type][base*10]/sm_used

def op_id_to_type(id):
    # inception v3 block_e: transformation
    if id == 0:
        return 0
    elif id == 1:
        return 6
    elif id == 2:
        return 1
    elif id == 3:
        return 4
    elif id == 4:
        return 5
    elif id == 5:
        return 3
    elif id == 6:
        return 2
    elif id == 7:
        return 3
    elif id == 8:
        return 2
    else:
        print("invalid operator id! Please check!")

dependency = [
    [-1],
    [-1],
    [-1],
    [-1],
    [2],
    [1],
    [1],
    [4],
    [4]
]

op_runtime_table = {
    # below are the type of operator, used for transform from id
    0: {
        # inception v3 block e: conv2d_1_1280_8_8+320_1_1+1_1_0_0
        10: 142.28,
        20: 77.157,
        30: 43.148,
        40: 33.612,
        50: 44.332,
        60: 35.788,
        70: 36.556,
        80: 25.731
    },
    1: {
        # inception v3 block e: conv2d_1_1280_8_8+448_1_1+1_1_0_0
        10: 130.73,
        20: 72.636,
        30: 86.636,
        40: 58.447,
        50: 44.063,
        60: 34.902,
        70: 37.5,
        80: 30.63
    },
    2: {
        # inception v3 block e: conv2d_1_384_8_8+384_3_1+1_1_1_0
        10: 106.61,
        20: 65.551,
        30: 52.265,
        40: 36.623,
        50: 37.673,
        60: 36.447,
        70: 31.75,
        80: 30.687
    },
    3: {
        # inception v3 block e: conv2d_1_384_8_8+384_1_3+1_1_0_1
        10: 115.42,
        20: 65.567,
        30: 52.037,
        40: 37.689,
        50: 37.842,
        60: 36.492,
        70: 32.889,
        80: 30.105
    },
    4: {
        # inception v3 block e: conv2d_1_1280_8_8+192_1_1+1_1_0_0
        10: 93.211,
        20: 57.846,
        30: 51.714,
        40: 40.982,
        50: 35.263,
        60: 35.039,
        70: 26.339,
        80: 25.094
    },
    5: {
        # inception v3 block e: conv2d_1_448_8_8+384_3_3+1_1_1_1
        10: 368.03,
        20: 234.18,
        30: 256.82,
        40: 206.89,
        50: 137.68,
        60: 137.09,
        70: 120.1,
        80: 16.95
    },
    6: {
        # inception v3 block e: conv2d_1_1280_8_8+384_1_1+1_1_0_0
        10: 119.47,
        20: 73.554,
        30: 58.399,
        40: 40.956,
        50: 36.169,
        60: 34.834,
        70: 33.362,
        80: 30.582
    }
}
