import redis
import csv
import pickle
import matplotlib.pyplot as plt
import time
import timeit
import matplotlib.animation as animation
import itertools

# ESTABLISH REDIS SERVER

r = redis.Redis(
    host='localhost',
    port=6379) 

# Headers:

file = open('/Users/marinatenhave/Downloads/AuxData_22-10-18_FS_OC05.csv') 
csvreader = csv.reader(file)
headers = next(csvreader)
print(headers)

# Other setup

fig, ax = plt.subplots()

file_path = '/Users/marinatenhave/Downloads/voltageplotter_aux_2.csv'
file = open(file_path, 'w')

writer = csv.DictWriter(file, headers)
writer.writeheader()

added = []

# plot arrays

# thermo_midd = []
# seconds = []

def aux_extract_save_plot(str=None):

    # WRITE TO FILE

    new_rows = []

    for key in r.keys():
        if 'aux_id' in key.decode('utf-8') and key not in added:
            key_dict_b = r.hgetall(key)
            key_dict = {}
            for onekey in key_dict_b:
                if onekey.decode('utf-8') in headers:
                    key_dict[onekey.decode('utf-8')] = key_dict_b[onekey].decode('utf-8')
            new_rows.append(key_dict)
            added.append(key)
            break

    print(new_rows)

    writer.writerows(new_rows)

    # for dict in new_rows:
    #     thermo_midd.append(float(dict['THERMO-Middle-Plate']))
    #     seconds.append(float(dict['Time']))

    # PLOT 3
    # print(seconds)
    # print(thermo_midd)

    # ax.scatter(seconds, thermo_midd, linewidths=0.01)
    # ax.set_xlabel("Time (seconds)")
    # ax.set_ylabel("Degrees (Celcius)")
    # ax.set_title("Thermo Middle Plate temperature over time")

    # plot_name = "MOXIE_Thermo-Mid_data_trial_n"
    # plt.savefig(plot_name) 
    # plt.show()

# Set up plot to call animate() function periodically
#aux_extract_save_plot()
# ani = animation.FuncAnimation(fig, aux_extract_save_plot(), fargs=(seconds, thermo_midd), interval=2000)
# plt.show()

while True:
    aux_extract_save_plot()
    time.sleep(1)
