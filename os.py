"""
Classical algorithms: SJF-NP, FCFS, RR
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
    """First Come, First Served"""
    waiting_arr = []
    response_arr = []
    turnaround_arr = []

    response = processes['new_to_ready'][0]

    for i in range(len(processes.index)):
        response_arr.append(response)
        waiting_arr.append(response - processes['new_to_ready'][i])
        turnaround_arr.append(processes['cpu_bursts'][i] +
                              processes['new_to_ready'][i] + waiting_arr[i])
        response += processes['cpu_bursts'][i]

    processes['response'] = response_arr
    processes['waiting'] = waiting_arr
    processes['turnaround'] = turnaround_arr

    return processes


def sjf_np(processes):
    """Shortest Job First - Non-preemptive"""
    processes.sort_values(by='cpu_bursts', inplace=True)
    return fcfs(processes).sort_index()


def rr(processes, qt):
    """Round Robin"""
    processes_mut = processes.copy()
    processes_mut['done'] = False

    waiting_arr = [0] * processes.shape[0]
    response_arr = [0] * processes.shape[0]
    turnaround_arr = [0] * processes.shape[0]
    acc = 0
    not_completed = True

    response = processes_mut['new_to_ready'][0]
    while not_completed:
        for i in range(len(processes.index)):
            idx = processes_mut.iloc[i].name
            if processes_mut.iloc[i].cpu_bursts > 0:
                processes_mut.set_value(idx, 'cpu_bursts', 
                    processes_mut.iloc[i].cpu_bursts - qt)
            else:
                processes_mut.set_value(idx, 'done', True)
        not_completed = processes_mut[processes_mut.done == True].empty

    processes_mut['response'] = response_arr
    processes_mut['waiting'] = waiting_arr
    processes_mut['turnaround'] = turnaround_arr

    return processes_mut.drop('done', axis=1)


def main():
    processes = create_processes()
    fcfs_result = fcfs(processes)
    sjf_np_result = sjf_np(processes)
    rr_result = rr(processes, 4)

if __name__ == '__main__':
    main()
