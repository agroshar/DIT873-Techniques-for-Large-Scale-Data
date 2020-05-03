import subprocess


if __name__ == '__main__':
    data_sizes = list(range(200_000, 1_010_000, 10_000))

    for size in data_sizes:
        command = 'head -n {} data/assignment3.dat'.format(size)
        with open('data/temp/{}.dat'.format(size), 'w') as output:
            subprocess.run(command.split(), stdout=output)

    for size in data_sizes:
        command = 'sbatch --cpus-per-task=8 /opt/local/bin/run_job.sh problem3-1.py data/temp/{}.dat {}'\
            .format(size, size)
        subprocess.run(command.split())
