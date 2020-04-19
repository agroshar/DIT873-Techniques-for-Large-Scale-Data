import subprocess
import time
from matplotlib import pyplot as plt


def run_experiment(cores_n):
    start = time.time()

    # command = 'python3 problem2-1.py -a 0.00001 -w {}'.format(cores_n)
    command = 'python3 problem2-2d.py -k 4 -s 100000 --c 4 -w {}'.format(cores_n)

    subprocess.call(command.split())

    end = time.time()

    timespan = end - start
    return timespan


def run_all(cores):
    performance = dict.fromkeys(cores)

    for n in performance.keys():
        performance[n] = run_experiment(n)
        
    speedup = dict.fromkeys(cores)
    baseline = performance[1]
    
    for n in speedup.keys():
        speedup[n] = baseline / performance[n]

    return speedup
    

def plot(speedup):
    plt.plot(*zip(*sorted(speedup.items())), label='Real')
    plt.plot([*speedup], [*speedup], label='Theoretical')
    plt.xticks(list(speedup.keys()))
    plt.xlabel('Number of cores')
    plt.ylabel('Speedup')
    plt.legend()
    plt.savefig('speedup_graph.png')
    # plt.show()


def main():
    cores = [1, 2, 4, 8, 16, 32]
    speedup = run_all(cores)
    plot(speedup)


if __name__ == '__main__':
    main()
