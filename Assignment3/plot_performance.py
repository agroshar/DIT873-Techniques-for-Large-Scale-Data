from matplotlib import pyplot as plt


def read_data(filename):
    performance = {}

    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                cores, time = line.split()
                performance[int(cores)] = float(time)

    return performance


def calculate_speedup(performance):
    baseline = performance[1]
    speedup = {cores: baseline / time for cores, time in performance.items()}

    return speedup


def plot(speedup):
    fig, (ax1, ax2) = plt.subplots(2, 1)

    ax1.plot(*zip(*sorted(speedup.items())), label='Real')
    ax1.plot([*speedup], [*speedup], label='Theoretical')
    ax1.set_xticks(list(speedup.keys()))
    ax1.set_ylabel('Speedup')
    ax1.legend()

    ax2.plot(*zip(*sorted(speedup.items())))
    ax2.set_xticks(list(speedup.keys()))
    ax2.set_xlabel('Number of cores')
    ax2.set_ylabel('Speedup')

    fig.savefig('output/speedup_graph.png')


if __name__ == '__main__':
    performance = read_data('output/time_measurements.txt')
    speedup = calculate_speedup(performance)
    plot(speedup)
