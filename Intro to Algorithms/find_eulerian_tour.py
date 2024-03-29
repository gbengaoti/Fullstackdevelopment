# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]

def find_eulerian_tour(graph):
    # your code here
    tour = []
    i = 0
    for x, y in graph:
        if i == 0:
            # first elements
            tour.append(x)
            tour.append(y)
        else:
            if x in tour:
                tour.append(y)
            elif y in tour:
                tour.append(x)
        i += 1
    print (tour)
    return tour

find_eulerian_tour([(1, 2), (2, 3), (3, 1)])

find_eulerian_tour([(0, 1), (1, 5), (1, 7), (4, 5),(4, 8), (1, 6), (3, 7), (5, 9),(2, 4), (0, 4), (2, 5), (3, 6), (8, 9)])
