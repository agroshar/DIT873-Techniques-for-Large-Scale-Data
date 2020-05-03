import sys
import subprocess

if __name__ == '__main__':
    for cores_n in [1, 2, 4, 8, 16, 32]:
        command = 'sbatch --cpus-per-task={} /opt/local/bin/run_job.sh '.format(cores_n) + \
                  'problem1d.py ' + \
                  '-d {} '.format(sys.argv[1]) + \
                  '-t True -l {}'.format(cores_n)
        subprocess.run(command.split())
