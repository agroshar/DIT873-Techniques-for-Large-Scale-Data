
import random
from pyspark import SparkContext
from math import ceil

LOAD_FILE_PATH = 'assignment3.dat'

def compute_stats():
    sc = SparkContext(master = 'local[4]')
    datFile = sc.textFile(LOAD_FILE_PATH)

    rdd = datFile.map(lambda l: l.split()).map(lambda t: float(t[2])).sortBy(lambda x: x)
    rdd_count = rdd.count()
    
    if rdd_count%2==0:
        mid_ind = int(rdd_count/2)
        mid_val1 = rdd.take(mid_ind)[mid_ind-1]
        mid_val2 = rdd.take(mid_ind+1)[mid_ind]
        rdd_median = (mid_val1 + mid_val2)/2
    else:
        mid_ind = int(ceil(rdd_count/2))
        rdd_median = rdd.take(mid_ind)[mid_ind-1]
    
    print('\nRDD Median: ', rdd_median)
    print('\n')


if __name__ == "__main__":
    compute_stats()