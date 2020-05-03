from mrjob.job import MRJob
import tempfile
from matplotlib.pyplot import hist
from time import process_time
import numpy as np
import argparse


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

    def configure_args(self):
        super(Summary, self).configure_args()
        self.add_passthru_arg('--group', '-g',
                              default=None,
                              type=int,
                              help="Group to filter the records")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', '-d',
                        default='data/assignment3.dat',
                        type=str,
                        help="Path to data file")
    parser.add_argument('--output_label', '-l',
                        default='',
                        type=str,
                        help="Label that is added to the output file")
    parser.add_argument('--time', '-t',
                        default=False,
                        type=bool,
                        help="Measuring time of the run and writing it to the file")
    parser.add_argument('--group', '-g',
                        default='',
                        type=str,
                        help="Group to filter the records")
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_arguments()

    job_args = [args.data]
    if args.group:
        job_args.append('-g {}'.format(args.group))
    job = Summary(args=job_args)
    runner = job.make_runner()

    if args.time:
        start = process_time()
        runner.run()
        measured_time = process_time() - start

        with open('output/time_measurements.txt', 'a') as f:
            f.write('\n{}   {}'.format(args.output_label, str(measured_time)))
    else:
        runner.run()

    for line in runner.stream_output():
        print(job.parse_output_line(line))
