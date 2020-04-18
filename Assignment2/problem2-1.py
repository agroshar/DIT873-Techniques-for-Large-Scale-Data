import multiprocessing as mp  # See https://docs.python.org/3/library/multiprocessing.html
import argparse  # See https://docs.python.org/3/library/argparse.html
import random
from math import pi, inf


def print_result(n_total, s_total, pi_est, error):
    """
    Prints nicely formatted result of a simulation.

    :param n_total: total number of steps
    :param s_total: number of successes
    :param pi_est: estimated pi value
    :param error: difference between estimated and real values
    """
    print("\n Steps\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, error))

def sample_pi(n, queue=None):
    """
    A worker function. Performs n steps of Monte Carlo simulation for estimating Pi/4.
    If a queue object is given then the result is put there.

    :param n: number of steps per worker
    :param queue: optional queue object
    :return: number of successes
    """
    random.seed()
    # print("Hello from a worker")
    s = 0

    for i in range(n):
        x = random.random()
        y = random.random()
        if x ** 2 + y ** 2 <= 1.0:
            s += 1

    if queue: queue.put(s)

    return s


def compute_pi_with_steps(workers, steps):
    """
    Computes pi using MC simulation with arbitrary maximum number of steps and threads.

    :param workers: number of threads
    :param steps: maximum number of steps in simulation
    """
    random.seed(1)
    n = int(steps / workers)

    p = mp.Pool(workers)
    s = p.map(sample_pi, [n] * workers)

    n_total = n * workers
    s_total = sum(s)
    pi_est = (4.0 * s_total) / n_total

    print_result(n_total, s_total, pi_est, pi - pi_est)


def compute_pi_with_accuracy(workers, accuracy):
    """
    Computes pi using MC simulation arbitrary number of threads until reaching given accuracy.

    :param workers: number of threads
    :param accuracy: goal accuracy of the calculated value
    """
    random.seed(1)
    default_steps = 1000
    n = int(default_steps / workers)

    queue = mp.Queue()

    s_total, n_total, pi_est, error = 0, 0, 0, inf

    while abs(error) > abs(accuracy):
        processes = mp.Pool(workers, sample_pi, (n, queue))
        processes.close()

        while not queue.empty(): s_total += queue.get()

        n_total += n * workers
        pi_est = (4.0 * s_total) / n_total

        error = pi - pi_est
        #print('Current accuracy: {}'.format(error), end='\r')

    print_result(n_total, s_total, pi_est, error)


def compute_pi(args):
    """
    Chooses the correct function to call based on given arguments.

    :param args: object containing parsed arguments
    """
    if args.steps:
        compute_pi_with_steps(args.workers, args.steps)
        return

    if args.accuracy:
        compute_pi_with_accuracy(args.workers, args.accuracy)
        return

    print('ERROR: This code should be unreachable!')


def parse_arguments():
    """
    Parses given arguments or evaluate default values.

    :return: object containing parsed arguments
    """
    parser = argparse.ArgumentParser(description='Compute Pi using Monte Carlo simulation.')

    parser.add_argument('--workers', '-w',
                        default=1,
                        type=int,
                        help='Number of parallel processes')
    mutex_group = parser.add_mutually_exclusive_group()
    mutex_group.add_argument('--steps', '-s',
                             type=int,
                             help='Number of steps in the Monte Carlo simulation')
    mutex_group.add_argument('--accuracy', '-a',
                             type=float,
                             help='Goal accuracy of the Monte Carlo simulation result')

    args = parser.parse_args()

    if not args.steps and not args.accuracy:
        parser.set_defaults(steps=1000)
        args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arguments()
    compute_pi(args)
