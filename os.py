"""
Classical algorithms: SJF, FCFS, RR
Criteria: Response time, waiting time, turnaround time,
throughput, cpu utilization
"""

import numpy as np
import pandas as pd


def create_processes():
    cpu_bursts = [np.random.randint(5, 15) for i in range(5)]
    new_to_ready = [5] * 5
    processes = pd.DataFrame({"cpu_bursts": cpu_bursts,
                              "new_to_ready": new_to_ready},
                             index=['p1', 'p2', 'p3', 'p4', 'p5'])
    return processes


def fcfs(processes):
    waiting_arr = []
    response_arr = []
    turnaround_arr = []

    response = processes['new_to_ready'][0]

    for i in range(len(processes.index)):
        response_arr.append(response)
        waiting_arr.append(response - processes['new_to_ready'][i])
        turnaround_arr.append(processes['cpu_bursts'][i]
                              + processes['new_to_ready'][i] + waiting_arr[i])
        response += processes['cpu_bursts'][i]

    processes['response'] = response_arr
    processes['waiting'] = waiting_arr
    processes['turnaround'] = turnaround_arr

    return processes


def sjf_np(processes):
    processes.sort_values(by='cpu_bursts', inplace=True)
    return fcfs(processes).sort_index()


def rr(processes, qt):
    pass


def main():
    processes = create_processes()
    fcfs_result = fcfs(processes)
    sjf_np_result = sjf_np(processes)
    rr_result = rr(processes, 4)

if __name__ == '__main__':
    main()
