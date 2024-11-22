import os

def calculate_thread_pool(task_type="io", max_threads=200):
    """
    Dynamically calculate the optimal number of threads based on the machine.

    :param task_type: "io" for I/O-bound tasks or "cpu" for CPU-bound tasks.
    :param max_threads: The maximum number of threads to use.
    :return: Optimal thread count.
    """
    num_cores = os.cpu_count()  # Number of logical cores (threads)
    
    if task_type == "io":
        # For I/O-bound tasks, use 5-10x the number of cores
        thread_count = num_cores * 5  # Start with 5x multiplier
    elif task_type == "cpu":
        # For CPU-bound tasks, match the number of cores
        thread_count = num_cores
    else:
        raise ValueError("Unknown task type. Use 'io' or 'cpu'.")

    # Cap the number of threads to prevent excessive usage
    return min(thread_count, max_threads)
