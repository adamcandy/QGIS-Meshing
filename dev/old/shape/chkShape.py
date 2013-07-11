import matplotlib.pyplot as pyplot

x = [0,0,1,1,0]

y = [0,1,1,0,0]
pyplot.plot(x,y)

x = [0,1,1,0,0]
y = [0.5,0.5,1.5,1.5,0.5]
pyplot.plot(x,y)
pyplot.xlim(-1,2)
pyplot.ylim(-1,2)
pyplot.show()
