
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
    print('RDD Median: ', rdd.median())
    print('RDD Standard deviation: ', rdd.stdev())
    print('Count: ', rdd.count())





if __name__ == "__main__":
    compute_stats()