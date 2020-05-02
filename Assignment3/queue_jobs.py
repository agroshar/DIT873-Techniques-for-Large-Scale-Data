import sys
import subprocess

if __name__ == '__main__':
    for cores_n in [1, 2, 4, 8, 16, 32]:
        command = 'sbatch --cpus-per-task={} /opt/local/bin/run_job.sh problem3-1.py {} {}'\
            .format(cores_n, sys.argv[1], cores_n)
        subprocess.call(command.split())
