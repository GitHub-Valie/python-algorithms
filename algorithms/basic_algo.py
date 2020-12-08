import numpy

# Data

array = numpy.random.rand(500)
data = array.tolist()

# Problem: we want to know if the value in the list is > 0.5 or not

for x in data:
    if x > 0.5:
        print('x: {} > 0.5'.format(round(x, 2)))
    
    else:
        print('x: {} < 0.5'.format(round(x, 2)))