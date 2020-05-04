from mrjob.job import MRJob
import tempfile
from matplotlib.pyplot import hist
import numpy as np


tempfile.tempdir = '/data/tmp'


class Summary(MRJob):
    def mapper_init(self):
        self.group = self.options.group

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

    def configure_args(self):
        super(Summary, self).configure_args()
        self.add_passthru_arg('--group', '-g',
                              default=None,
                              type=int,
                              help="Group to filter the records")


if __name__ == '__main__':
    Summary.run()
