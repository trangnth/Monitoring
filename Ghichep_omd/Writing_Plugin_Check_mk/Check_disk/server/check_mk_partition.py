#!/usr/bin/python3.5

def perfometer_check_mk_partition(row, check_command, perf_data):
    state = int(perf_data[0][0])
    color = ""

    if state == 2:
        color = "#ff0000"
    elif state == 1:
        color = "#ffff00"
    elif state == 0:
        color = "#00ff00"

    return "{0:.1f}%".format(perf_data[0][1]), perfometer_linear(int(perf_data[0][1]), color)

perfometers["check_mk-check_mk_partition"] = perfometer_check_mk_partition
