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
line_p5, = ax1.plot([], [], lw=2)
line_p4, = ax1.plot([], [], lw=2)
ax1.set_xlabel('SW_TIME (seconds)')
ax1.set_ylabel('Pressure (millibar)')
ax1.set_title("Pressure over time")

fig, ax2 = plt.subplots()
line_tt, = ax2.plot([], [], lw=2)
line_tb, = ax2.plot([], [], lw=2)
ax2.set_xlabel("SW_TIME (seconds)")
ax2.set_ylabel("Degrees (Celcius)")
ax2.set_title("Top and Bottom temperature over time")

file_path = 'MOXIE_data_trial_n.csv'
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

def data_gen():

    new_rows = []

    for key in r.keys():
        if 'csv_id' in key.decode('utf-8') and key not in added:
            key_dict_b = r.hgetall(key)
            key_dict = {}
            for akey, value in key_dict_b.items():
                key_dict[akey.decode('utf-8')] = value
            new_rows.append(key_dict)
            yield key_dict
    
    writer.writerows(new_rows)

def run(key_dict):
    # update the data
    p4.append(float(key_dict['P4'])*1000)
    p5.append(float(key_dict['P5'])*1000)
    sw_time.append(float(key_dict['SW_TIME']))
    tt_lc.append(float(key_dict['TT_LC']))
    tb_lc.append(float(key_dict['TB_LC']))

    line_p5.set_data(sw_time, p5)
    line_p4.set_data(sw_time, p4)
    line_tt.set_data(sw_time, tt_lc)
    line_tb.set_data(sw_time, tb_lc)

    return line_p5, line_p4, line_tt, line_tb

def init():

    # ax.set_ylim(-1.1, 1.1)
    # ax.set_xlim(0, 1)
    del sw_time[:]
    del p5[:]
    del p4[:]
    del tt_lc[:]
    del tb_lc[:]

    line_p5.set_data(sw_time, p5)
    line_p4.set_data(sw_time, p4)
    line_tt.set_data(sw_time, tt_lc)
    line_tb.set_data(sw_time, tb_lc)
    
    return line_p5, line_p4, line_tt, line_tb

# main_extract_save_plot()
ani = FuncAnimation(fig, run, data_gen, interval=1000, init_func=init, blit=True)
# ani = FuncAnimation(fig, run, data_gen, interval=1000, init_func=init)
plt.show()


