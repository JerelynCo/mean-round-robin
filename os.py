"""
Classical algorithms: SJF, FCFS, RR
Criteria: Response time, waiting time, turnaround time, throughput, cpu utilization
"""
import pandas as pd
import numpy as np


def create_processes():
    processes = pd.Series([np.random.randint(5, 15)
                           for i in range(5)], index=['p1', 'p2', 'p3', 'p4', 'p5'])
    return processes


def fcfs(processes):
    clock_cycles = 0


def main():
	results = pd.DataFrame();
    processes = create_processes()
    fcfs(processes)
    return 0
