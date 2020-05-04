
import random
from pyspark import SparkContext

LOAD_FILE_PATH = 'assignment3.dat'

def compute_stats():
    sc = SparkContext(master = 'local[4]')
    datFile = sc.textFile(LOAD_FILE_PATH)

    rdd = datFile.map(lambda l: l.split()).map(lambda t: float(t[2]))

    print('\nRDD Min: ', rdd.min())
    print('RDD Max: ', rdd.max())
    print('RDD Mean: ', rdd.mean())
    print('RDD Standard deviation: ', rdd.stdev())

    bin_sizes, counts = rdd.histogram(10)
    print('RDD Histogram - bin_sizes and counts: ', bin_sizes, counts)
    print('\n')


if __name__ == "__main__":
    compute_stats()