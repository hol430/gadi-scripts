#!/usr/bin/env python3

from sys import argv, exit

if __name__ == "__main__":
    is_help = "-h" in argv or "--help" in argv
    if len(argv) != 3 or is_help:
        print(f"Usage: {argv[0]} <# gridcells> <queue>")
        exit(0 if is_help else 1)

from math import ceil
from gadi_queues import *

def find_optimal_cpus(N, M, max_multiplier=10):
    """
    Find optimal CPU counts for distributing N gridcells across CPUs,
    where the number of CPUs must be a multiple of M.

    Args:
        N (int): Total number of gridcells.
        M (int): Node size (number of CPUs per node).
        max_multiplier (int): Maximum multiple of M to consider for CPUs.

    Returns:
        list: A sorted list of tuples (CPUs, imbalance), where
              - CPUs is a valid CPU count (multiple of M),
              - imbalance is the leftover cpus which will be idle at end-of-job.
    """
    results = []
    for k in range(1, max_multiplier + 1):
        cpus = k * M
        imbalance = cpus - (N % cpus)
        results.append((cpus, imbalance))
    # Sort by imbalance, then by CPUs (to prioritize fewer CPUs for same imbalance)
    return sorted(results, key=lambda x: (x[1], x[0]))

def print_optimal_cpus(N, M, max_multiplier=10):
    """
    Print the optimal CPU counts with their corresponding imbalance.

    Args:
        N (int): Total number of gridcells.
        M (int): Node size (number of CPUs per node).
        max_multiplier (int): Maximum multiple of M to consider for CPUs.
    """
    results = find_optimal_cpus(N, M, max_multiplier)
    print(f"Optimal CPU configurations for N={N} gridcells and M={M} CPUs per node:")
    print(" CPUs | Imbalance | Efficiency")
    print("------+-----------+-----------")
    for cpus, imbalance in results:
        # Percentage of CPUs effectively utilised.
        efficiency = (N - imbalance) / N * 100
        print(f"{cpus:5} | {imbalance:9} | {efficiency:9.2f}%")
    print("Imbalance is the number of CPUs left idle at the end of the job while the remaining CPUs run one extra gridcell. This assumes that all gridcells take an equal amount of time to complete.")

if __name__ == "__main__":
    # Total number of gridcells.
    ngridcell = int(argv[1])

    # The job submission queue.
    queue_name = argv[2]

    # Get number of CPUs per node in this queue.
    queue = get_queue(queue_name)

    # Don't allow more than 1 CPU per gridcell (obviously).
    max_multiplier = int(ceil(ngridcell / queue.cpus_per_node))

    # Find optimal configuration and print results.
    print_optimal_cpus(ngridcell, queue.cpus_per_node, max_multiplier)
