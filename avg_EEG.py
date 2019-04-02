import math
import numpy as np
from matplotlib import pyplot as plt

def data_parsing(filename):
    keywords = ["Interval", "Excel", "Time", "Date", "Channel", "Range"]
    with open(filename, "r") as f:
        data = f.readlines()
        table = []
        for i in data[6:]:
            if any (word in i for word in keywords): break
            table += [i[:-1].split("\t")]
    return table
    
def transform_table(table,start_trim,end_trim):
    '''
    transform the table such that:
    col: each data point
    row: each timeframe (per sec)
    then flip the col and row
    '''
    new_table = [[] for i in range(0,math.floor(float(table[-1][0]))+1)]
    for i in table:
        new_table[math.floor(float(i[0]))] += [i[2]]
    return np.stack(new_table[start_trim:-end_trim], axis=1)
    
def sync_avg(table, time_start_trim, time_end_trim):
    '''
    for all EEG timeframe (per sec), do an avg of every data point
    '''
    new_table = transform_table(table,start_trim=6,end_trim=9)
    if time_start_trim != 0 and time_end_trim != 0:
        new_table = new_table[time_start_trim: -time_end_trim]
    avg_graph = []
    for row in new_table:
        avg_graph+=[np.mean([float(j) for j in row if j != "NaN"])]
    plt.plot(avg_graph)
    plt.show()
    
table = data_parsing("Part D Txt Data.txt")
sync_avg(table, time_start_trim=100, time_end_trim=100)