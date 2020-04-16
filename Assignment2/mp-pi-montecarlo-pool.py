import multiprocessing  # See https://docs.python.org/3/library/multiprocessing.html
import argparse  # See https://docs.python.org/3/library/argparse.html
import random
from math import pi


def sample_pi(n):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""
    random.seed()
    print("Hello from a worker")
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x ** 2 + y ** 2 <= 1.0:
            s += 1
    return s


def compute_pi_with_steps(workers, steps):
    random.seed(1)
    n = int(steps / workers)

    p = multiprocessing.Pool(workers)
    s = p.map(sample_pi, [n] * workers)

    n_total = n * workers
    s_total = sum(s)
    pi_est = (4.0 * s_total) / n_total
    print(" Steps\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, pi - pi_est))


def compute_pi_with_accuracy(workers, accuracy):
    print("xD")


def compute_pi(args):
    if args.steps:
        compute_pi_with_steps(args.workers, args.steps)
        return

    if args.accuracy:
        compute_pi_with_accuracy(args.workers, args.accuracy)
        return

    print('ERROR: This code should be unreachable!')


def parse_arguments():
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
