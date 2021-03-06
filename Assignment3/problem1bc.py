from mrjob.job import MRJob
import tempfile
from matplotlib.pyplot import hist
from time import process_time
import numpy as np
import sys


tempfile.tempdir = '/data/tmp'


class Summary(MRJob):
    def mapper(self, _, record):
        _, group, value = record.split()

        if self.group is None or self.group == int(group):
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
    output_param = sys.argv[-1]
    sys.argv = sys.argv[:2]

    start = process_time()
    Summary.run()
    measured_time = process_time() - start

    with open('output/time_measurements.txt', 'a') as f:
        f.write('\n{}   {}'.format(str(output_param), str(measured_time)))
