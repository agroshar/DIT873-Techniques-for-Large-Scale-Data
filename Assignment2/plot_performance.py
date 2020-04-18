import subprocess
import time
from matplotlib import pyplot as plt


def run_experiment(cores_n, accuracy):
    start = time.time()
    subprocess.call(['python3', 'problem2-1.py',
                     '-w', str(cores_n),
                     '-a', str(accuracy)])
    end = time.time()

    timespan = end - start
    return timespan


def run_all(cores, accuracy):
    performance = dict.fromkeys(cores)

    for n in performance.keys():
        performance[n] = run_experiment(n, accuracy)
        
    speedup = dict.fromkeys(cores)
    baseline = performance[1]
    
    for n in speedup.keys():
        speedup[n] = baseline / performance[n]

    return speedup
    

def plot(speedup):
    plt.plot(*zip(*sorted(speedup.items())), label='Real')
    plt.plot([*speedup], [*speedup], label='Theoretical')
    plt.xlabel('Number of cores')
    plt.ylabel('Speedup')
    plt.legend()
    plt.savefig('speedup_graph.png')
    # plt.show()


def main():
    cores = [1, 2, 4, 8, 16, 32]
    accuracy = 1e-6
    speedup = run_all(cores, accuracy)
    plot(speedup)


if __name__ == '__main__':
    main()
