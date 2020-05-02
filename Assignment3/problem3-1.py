from mrjob.job import MRJob
import tempfile
from statistics import mean, stdev
import matplotlib.pyplot as plt
from time import process_time
import sys


tempfile.tempdir = '/data/tmp'


class Summary(MRJob):
    def mapper(self, _, line):
        _, _, value = line.split()
        yield 'val', float(value)

    def reducer(self, _, values):
        val_list = list(values)

        yield 'mean', mean(val_list)
        yield 'stdev', stdev(val_list)
        yield 'min', min(val_list)
        yield 'max', max(val_list)

        bin_sizes, edges, _ = plt.hist(val_list, bins=10)

        yield 'hist', (bin_sizes, edges)


if __name__ == '__main__':
    cores_n = sys.argv[-1]
    sys.argv = sys.argv[:2]

    start = process_time()
    Summary.run()
    measured_time = process_time() - start

    with open('time_measurements.txt', 'a') as f:
        f.write('\n{}   {}'.format(str(cores_n), str(measured_time)))
