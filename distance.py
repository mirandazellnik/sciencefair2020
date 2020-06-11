import numpy

# Find Edit Distance between two strings
def dist(a, b):
    sizex = len(a) + 1
    sizey = len(b) + 1
    matrix = numpy.zeros((sizex, sizey))
    for x in range(sizex):
        matrix[x,0] = x
    for y in range(sizey):
        matrix[0,y] = y

    for y in range(1, sizey):
        for x in range(1, sizex):
            cost = 0
            if a[x-1] != b[y-1]:
                cost = 2
            matrix[x,y] = min(
                matrix[x-1, y] + 1,
                matrix[x, y-1] + 1,
                matrix[x-1, y-1] + cost
            )
            
    return int(matrix[sizex - 1, sizey - 1])
