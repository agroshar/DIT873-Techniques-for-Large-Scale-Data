#!/usr/bin/env python
#
# File: kmeans.py
# Author: Alexander Schliep (alexander@schlieplab.org)
#
#
import logging
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import time
import multiprocessing as mp
from statistics import mean


def generateData(n, c):
    logging.info(f"Generating {n} samples in {c} classes")
    X, _ = make_blobs(n_samples=n, centers=c, cluster_std=1.7, shuffle=False,
                      random_state=2122)

    return X


def nearestCentroid(datum, centroids):
    # norm(a-b) is Euclidean distance, matrix - vector computes difference
    # for all rows of matrix
    dist = np.linalg.norm(centroids - datum, axis=1)
    return np.argmin(dist), np.min(dist)


def workerTask(worker_data):
    data_chunk, centroids = worker_data

    n = len(data_chunk)
    k = len(centroids)

    cluster_sizes = np.zeros(k, dtype=int)
    variation = 0
    new_centroids = np.zeros((k, 2))
    assignments_chunk = np.zeros(n)

    for i in range(n):
        cluster, dist = nearestCentroid(data_chunk[i], centroids)

        cluster_sizes[cluster] += 1
        variation += dist ** 2
        assignments_chunk[i] = cluster

        new_centroids[cluster] += data_chunk[i]

    return cluster_sizes, variation, new_centroids, assignments_chunk


def evaluate_results(clustering_results, k):
    cluster_sizes_sum = np.zeros(k, dtype=int)
    variation_sum = 0
    new_centroids_sum = np.zeros((k, 2))
    assignments = []

    for (cluster_sizes, variation, new_centroids, assignments_chunk) in clustering_results:
        cluster_sizes_sum += cluster_sizes
        variation_sum += variation
        new_centroids_sum += new_centroids
        assignments += assignments_chunk.tolist()

    return cluster_sizes_sum, variation_sum, new_centroids_sum, assignments


def kmeans(k, data, nr_iter=100, workers=1):
    N = len(data)

    # Choose k random data points as centroids
    centroids = data[np.random.choice(np.array(range(N)), size=k, replace=False)]
    logging.debug("Initial centroids\n", centroids)

    # The cluster index: c[i] = j indicates that i-th datum is in j-th cluster
    c = np.zeros(N, dtype=int)

    logging.info("Iteration\tVariation\tDelta Variation")
    total_variation = 0.0
    times = []

    for j in range(nr_iter):
        logging.debug("=== Iteration %d ===" % (j + 1))
        start_part_time = time.perf_counter()

        workers_data = [(data_chunk, centroids) for data_chunk in np.array_split(data, workers)]
        processes = mp.Pool(workers)
        clustering_results = processes.map(workerTask, workers_data)

        cluster_sizes_sum, variation_sum, new_centroids_sum, c = evaluate_results(clustering_results, k)

        delta_variation = -total_variation
        total_variation = variation_sum
        delta_variation += total_variation
        logging.info("%3d\t\t%f\t%f" % (j, total_variation, delta_variation))

        centroids = new_centroids_sum / cluster_sizes_sum.reshape(-1, 1)

        times.append(time.perf_counter() - start_part_time)

        logging.debug(cluster_sizes_sum)
        logging.debug(c)
        logging.debug(centroids)

    print('Average time measured: {}'.format(mean(times)))
    return total_variation, c


def computeClustering(args):
    if args.verbose:
        logging.basicConfig(format='# %(message)s', level=logging.INFO)
    if args.debug:
        logging.basicConfig(format='# %(message)s', level=logging.DEBUG)

    X = generateData(args.samples, args.classes)

    start_time = time.time()
    total_variation, assignment = kmeans(args.k_clusters, X, nr_iter=args.iterations, workers=args.workers)
    end_time = time.time()

    logging.info("Clustering complete in %3.2f [s]" % (end_time - start_time))
    print(f"Total variation {total_variation}")

    if args.plot:  # Assuming 2D data
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.scatter(X[:, 0], X[:, 1], c=assignment, alpha=0.2)
        plt.title("k-means result")
        # plt.show()
        fig.savefig(args.plot)
        plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Compute a k-means clustering.',
        epilog='Example: kmeans.py -v -k 4 --samples 10000 --classes 4 --plot result.png'
    )
    parser.add_argument('--workers', '-w',
                        default='1',
                        type=int,
                        help='Number of parallel processes to use')
    parser.add_argument('--k_clusters', '-k',
                        default='3',
                        type=int,
                        help='Number of clusters')
    parser.add_argument('--iterations', '-i',
                        default='100',
                        type=int,
                        help='Number of iterations in k-means')
    parser.add_argument('--samples', '-s',
                        default='10000',
                        type=int,
                        help='Number of samples to generate as input')
    parser.add_argument('--classes', '-c',
                        default='3',
                        type=int,
                        help='Number of classes to generate samples from')
    parser.add_argument('--plot', '-p',
                        type=str,
                        help='Filename to plot the final result')
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Print verbose diagnostic output')
    parser.add_argument('--debug', '-d',
                        action='store_true',
                        help='Print debugging output')
    args = parser.parse_args()
    computeClustering(args)
