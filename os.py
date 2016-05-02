"""
Classical algorithms: SJF-NP, FCFS, RR
Criteria: Response time, waiting time, turnaround time,
throughput, cpu utilization
"""

import numpy as np
import pandas as pd
import sys

cc = 30


def get_throughput(df):
    return len(df[df['turnaround'] < cc])


def create_processes():
    cpu_bursts = [np.random.randint(5, 15) for i in range(5)]
    new_to_ready = [5] * 5
    processes = pd.DataFrame({"cpu_bursts": cpu_bursts,
                              "new_to_ready": new_to_ready},
                             index=['p1', 'p2', 'p3', 'p4', 'p5'])
    return processes


def fcfs(processes, algo):
    """First Come, First Served"""
    processes = processes.copy()
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

    print("{}: Throughput of {} with clock cycle benchmark of {}".format(
        algo, get_throughput(processes), cc))
    return processes


def sjf_np(processes, algo):
    """Shortest Job First - Non-preemptive"""
    processes = processes.copy()
    processes.sort_values(by='cpu_bursts', inplace=True)

    return fcfs(processes, algo).sort_index()


def rr(processes, qt, algo, mean_variant=False, modified_mean_variant=False):
    """Round Robin"""
    processes_mut = processes.copy()
    processes_mut['started'] = False
    processes_mut['done'] = False

    response_arr = list(processes_mut['new_to_ready'])
    turnaround_arr = list(processes_mut['new_to_ready'])
    waiting_arr = [0] * processes.shape[0]
    acc = 0
    not_completed = True

    while not_completed:
        for i in range(len(processes_mut.index)):
            idx = processes_mut.iloc[i].name
            cpu_burst = processes_mut.iloc[i]['cpu_bursts']
            # Mean round robin
            if mean_variant:
                qt = np.around(
                    processes_mut[processes_mut.done == False][
                        'cpu_bursts']
                    .mean())
            # Modified mean round robin
            if modified_mean_variant:
                qt = np.ceil(
                    processes_mut[processes_mut.done == False]['cpu_bursts']
                    .mean())

            if not processes_mut.loc[idx]['started']:
                response_arr[i] += acc
                processes_mut.set_value(idx, 'started', True)
            if cpu_burst > 0:
                result = cpu_burst - qt
                if result <= 0:
                    result = 0
                    acc += cpu_burst
                    turnaround_arr[i] += acc
                else:
                    acc += qt
                processes_mut.set_value(idx, 'cpu_bursts',
                                        result)
            else:
                processes_mut.set_value(idx, 'done', True)

        not_completed = False in processes_mut.done.unique()

    processes_mut['cpu_bursts'] = processes['cpu_bursts']
    processes_mut['response'] = response_arr
    processes_mut['turnaround'] = turnaround_arr
    processes_mut['waiting'] = processes_mut['turnaround'] - \
        processes_mut['cpu_bursts'] - processes_mut['new_to_ready']

    print("{}: Throughput of {} with clock cycle benchmark of {}".format(
        algo, get_throughput(processes_mut), cc))
    return processes_mut.drop(['done', 'started'], axis=1)


def main():
    for i in range(3):
        processes = create_processes()

        print("\n*****Throughput values per algorithm*****")

        ## Redirecting print stream to output stream
        orig_stdout = sys.stdout
        f = open("results/throughputs_{}.txt".format(i), 'w')
        sys.stdout = f

        ## Initializing results // prints the throughputs
        fcfs_result = fcfs(processes, "fcfs")
        sjf_np_result = sjf_np(processes, "sfj")
        rr_result = rr(processes, 4, "rr")
        orig_mean_rr_result = rr(processes, 0, "orig_mean_rr", mean_variant=True )
        mod_mean_rr_result = rr(processes, 0, "mod_mean rr", modified_mean_variant=True)

        ## Closing of output stream and returning the print stream
        sys.stdout = orig_stdout
        f.close()

        ## Displaying of evaluations
        print("\n*****Performance Evaluation per Algorithm*****")
        print("First Come, First Served")
        print(fcfs_result)
        print("\nShortest Job First - Non-Preemptive")
        print(sjf_np_result)
        print("\nRound Robin - QT = 4")
        print(rr_result)
        print("\nRound Robin with Dynamic QT via Average CPU Burst (Original)")
        print(orig_mean_rr_result)
        print("\nRound Robin with Dynamic QT via Average CPU Burst (Modified)")
        print(mod_mean_rr_result)

        ## Saving of results to CSV
        fcfs_result.to_csv("results/fcfs_result_{}".format(i))
        sjf_np_result.to_csv("results/sjf_np_result_{}".format(i))
        rr_result.to_csv("results/rr_result_{}".format(i))
        orig_mean_rr_result.to_csv("results/orig_mean_rr_result_{}".format(i))
        mod_mean_rr_result.to_csv("results/mod_mean_rr_result_{}".format(i))


if __name__ == '__main__':
    main()
