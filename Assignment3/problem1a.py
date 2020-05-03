from mrjob.job import MRJob
import tempfile
from matplotlib.pyplot import hist
from time import process_time
import numpy as np


tempfile.tempdir = '/data/tmp'


class Summary(MRJob):
    def mapper(self, _, line):
        _, _, value = line.split()
        yield 'val', float(value)

    def reducer(self, _, values):
        val_list = np.fromiter(values, dtype=float)

        yield 'mean', np.mean(val_list)
        yield 'stdev', np.std(val_list)
        yield 'min', np.min(val_list)
        yield 'max', np.max(val_list)

        bin_sizes, edges, _ = hist(val_list, bins=10)

        yield 'hist', (bin_sizes, edges)


if __name__ == '__main__':
    start = process_time()
    Summary.run()
    measured_time = process_time() - start
    print('time: {} s'.format(measured_time))
