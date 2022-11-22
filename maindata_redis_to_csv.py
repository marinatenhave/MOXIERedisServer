import redis
import csv
import pickle
import matplotlib.pyplot as plt
import time
import timeit
from matplotlib.animation import FuncAnimation

# ESTABLISH REDIS SERVER

r = redis.Redis(
    host='localhost',
    port=6379) 

# FIND HEADERS

file = open('/Users/marinatenhave/Downloads/OX__0535_0714394410EDR0000261222MOXI00114J02.CSV') 
csvreader = csv.reader(file)
headers = next(csvreader)
headers = headers[3:126]

# other setup

fig, ax1 = plt.subplots()
ax1.set_xlabel('SW_TIME (seconds)')
ax1.set_ylabel('Pressure (millibar)')
ax1.set_title("Pressure over time")

fig, ax2 = plt.subplots()
ax2.set_xlabel("SW_TIME (seconds)")
ax2.set_ylabel("Degrees (Celcius)")
ax2.set_title("Top and Bottom temperature over time")

file_path = '/Users/marinatenhave/Downloads/voltageplotter.csv'
file = open(file_path, 'w')

writer = csv.DictWriter(file, headers)

writer.writeheader()

added = []

# plot arrays

p4 = []
p5 = []
sw_time = []
tt_lc = []
tb_lc = []

def main_extract_save_plot(str=None):

    # WRITE TO FILE

    new_rows = []

    for key in r.keys():
        if 'csv_id' in key.decode('utf-8') and key not in added:
            key_dict_b = r.hgetall(key)
            key_dict = {}
            for akey, value in key_dict_b.items():
                key_dict[akey.decode('utf-8')] = value
            new_rows.append(key_dict)
            break

    print(len(key_dict_b), len)
    writer.writerows(new_rows)

    # PLOT

    # for dict in new_rows:
    #     p4.append(float(dict['P4'])*1000)
    #     p5.append(float(dict['P5'])*1000)
    #     sw_time.append(float(dict['SW_TIME']))
    #     tt_lc.append(float(dict['TT_LC']))
    #     tb_lc.append(float(dict['TB_LC']))

    # print('p4', len(p4))
    # print('p5', len(p5))
    # print('swtime', len(sw_time))
    # print('TB', len(tb_lc))
    # print('TT', len(tt_lc))

    # # PLOT 1

    # ax1.scatter(sw_time, p5, color='r', linewidths=0.01, label='P5')
    # ax1.scatter(sw_time, p4, color='b', linewidths=0.01, label='P4')
    # ax1.legend()

    # plot_name = "MOXIE_p4_p5_data_trial_n"
    # plt.savefig(plot_name) 

    # # PLOT 2
    # print(tt_lc)
    # print(tb_lc)
    # ax2.scatter(sw_time, tt_lc, color='r', linewidths=0.01, label='TT_LC')
    # ax2.scatter(sw_time, tb_lc, color='b', linewidths=0.01, label='TB_LC')
    # ax2.legend()

    # plot_name = "MOXIE_TB_TT_data_trial_n"
    # plt.savefig(plot_name) 

    # plt.show()

# # main_extract_save_plot()
# ani = FuncAnimation(fig, main_extract_save_plot, interval=1000)
# plt.show()

while True:
    main_extract_save_plot()
    time.sleep(1)
