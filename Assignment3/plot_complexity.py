from matplotlib import pyplot as plt
from sys import argv
import numpy as np
from scipy import optimize


def read_data(filename):
    performance = {}

    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                size, time = line.split()
                performance[int(size)] = float(time)

    sizes, times = zip(*sorted(performance.items()))

    return sizes, times


def find_fit(sizes, times, degree):
    fit_poly = np.poly1d(np.polyfit(sizes, times, degree))
    return fit_poly


def plot(sizes, times, fit_poly):
    plt.plot(sizes, times, label='Measured time')
    plt.plot(sizes, fit_poly(sizes), '--', label=str(fit_poly))

    plt.xlabel('Number of records')
    plt.ylabel('Time [s]')
    plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    plt.xticks(sizes[0::10])
    plt.legend()

    plt.savefig('output/complexity_graph.png')


if __name__ == '__main__':
    sizes, times = read_data(argv[1])
    fit_poly = find_fit(sizes, times, int(argv[2]))
    plot(sizes, times, fit_poly)
