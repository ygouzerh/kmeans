#!/usr/bin/env python3

from scipy.spatial import distance
from random import choice, randint
import matplotlib.pyplot as pyplot
from time import sleep

LOG = True
GRAPH = False

def log(message):
    if LOG:
        print(message)

def show_clusters(clusters, centroids):
    """
        Show clusters
    """
    if GRAPH:
        for cluster in clusters:
            pyplot.plot([point[0] for point in cluster], [point[1] for point in cluster], 'o-')
        pyplot.plot([point[0] for point in centroids], [point[1] for point in centroids], 'o-')
        pyplot.show()

def kmeans(k_clusters_number, centroids, clusters, steps):
    """
        Start with centroids = []
        and clusters = [[(a1, b1), (a2, b2)], [empty], [empty],...]
    """
    log("\nITERATION NUMBER : {}".format(steps))
    show_clusters(clusters, centroids)
    if centroids == []:
        centroids = [[] for _ in range(k_clusters_number)]
        log("-- STEP INITIAL -- ")
        # Choose first centroid
        centroids[0] = choice(clusters[0])
        log("Centroid 0 : {}".format(centroids[0]))
        for i in range(1, k_clusters_number):
            # Choose second centroid
            centroids[i] = choice(clusters[0])
            while centroids[i] == centroids[0]:
                centroids[i] = choice(clusters[0])
        log("We choose the centroids : {}".format(centroids))
    # Stop condition
    if steps == 0:
        # Clean clusters from centroids
        for cluster in clusters:
            for centroid in centroids:
                if centroid in cluster:
                    cluster.remove(centroid)
        return clusters
    # STEP ONE : For all points, find the closest centroid and append the point to his cluster
    log("-- STEP ONE -- ")
    new_clusters = [[] for _ in range(k_clusters_number)]
    for cluster in clusters:
        for point in cluster:
            # [(index of centroid, distance to this centroid), (...,...),...]
            distances = []
            is_centroid = False
            for index, centroid in enumerate(centroids):
                distances.append((index, distance.euclidean(point, centroid)))
            # Add to the cluster with the min distance
            new_clusters[min(distances, key=lambda d: d[1])[0]].append(point)
    # Add the centroid to the clusters
    for index, centroid in enumerate(centroids):
        new_clusters[index].append(centroid)
    # Update the cluster list
    clusters = new_clusters.copy()
    # STEP TWO : Calculate the new centroids
    log("-- STEP TWO -- ")
    new_centroids = []
    # If it is 2d, 3d, ...
    dimensions = len(clusters[0][0])
    for cluster in clusters:
        centroid = [[] for _ in range(dimensions)]
        cluster_size = len(cluster)
        for dimension in range(dimensions):
            sum_dimension = 0
            for point in cluster:
                sum_dimension += point[dimension]
            centroid[dimension] = sum_dimension / cluster_size
        log("For cluster {}, we have the centroids : {}".format(cluster, tuple(centroid)))
        new_centroids.append(tuple(centroid))
    centroids = new_centroids.copy()
    steps -= 1
    return kmeans(k_clusters_number, centroids, clusters, steps)

k_clusters_number = 3
centroids = []
clusters = [[(1.1, 60), (8.2, 20), (4.2, 35), (1.5, 21), (7.6, 15), (2.0, 55), (3.9, 39)]]
#clusters = [[(randint(0, 60), randint(0, 60)) for _ in range(30)]]
steps = 5
clusters = kmeans(k_clusters_number, centroids, clusters, steps)
print("\n----- RESULT -----")
for index, cluster in enumerate(clusters):
    print("\nCluster {}:".format(index))
    print(cluster)
