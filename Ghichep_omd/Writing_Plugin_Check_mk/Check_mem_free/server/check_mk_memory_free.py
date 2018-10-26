#!/usr/bin/python3.5

#def perfometer_check_mk_memory_free(row, check_command, perf_data):
#    return 'Hello World! :-)', '<table><tr>' \
#                               + perfometer_td(20, '#fff') \
#                               + perfometer_td(80, '#ff0000') \
#                               + '</tr></table>'

#perfometers['check_mk-check_mk_memory_free'] = perfometer_check_mk_memory_free


#def perfometer_check_mk_info(row, check_command, perf_data):
#    number = int(perf_data[0][1][3])
#    color = "#00ff00"
#    return number, perfometer_linear(100,color)

#perfometers['check_mk-check_mk_memory_free'] = perfometer_check_mk_info

def perfometer_check_mk_memory_free(row, check_command, perf_data):
    state = int(perf_data[0][0])
    
    color = ""
    if state == 2:
        color = "#ff0000"
    elif state == 1:
        color = "#ffff00"
    elif state == 0:
        color = "#00ff00"

    return "Used {0:.1f}%".format(100 - perf_data[0][1]), perfometer_linear(100 - int(perf_data[0][1]), color)

perfometers["check_mk-check_mk_memory_free"] = perfometer_check_mk_memory_free
