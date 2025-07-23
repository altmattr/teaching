import numpy
import matplotlib.pyplot as plt

rainfall     = numpy.array([11.4,0,0.4,0,0,2,0.2,0.2,0.2,0,0,0,3,3.8,13.2,0,0,0,0.2,0,0,0,2.6])

upper_molo   = 5*rainfall # what would it look like to slow the rainfall?
googong      = 10*rainfall

# googong resevoir stores up to 80, then dumps 20 in a day if it gets over that and catastrophically fails after 2000.
def googong_res(history):
    sum = 0
    res = [0] * len(history)
    for (i, h) in enumerate(history):
      sum = sum + h
      if (sum < 80):
        res[i] = 0
      elif (sum < 2000):
        res[i] = 20
        sum = sum - 20
      else:
        res[i] = sum
        sum = 0
    return res

lower_quean  = googong_res(googong) + (1 * rainfall)

jerra = 2*rainfall
central_molo = jerra + lower_quean + upper_molo + (3*rainfall)

# gets to 200 and then stays there
def burley(history):
    capacity = 3000
    sum = 0
    res = [0] * len(history)
    summ = [0] * len(history)
    for (i, h) in enumerate(history):
      sum = sum + h
      if (sum <= capacity):
        res[i] = 0
      else:
        res[i] = sum - capacity
        sum = capacity
      summ[i] = sum
    return res, summ

lower_molo = burley(central_molo)[0] + 0.8*rainfall
print(lower_molo)
print(burley(central_molo)[1])
fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(numpy.linspace(0,1, len(rainfall)), lower_molo, label="lower molo", scaley=(0,150))
ax1.plot(numpy.linspace(0,1, len(rainfall)), central_molo, label="central molo",scaley=(0,150))
ax2.plot(numpy.linspace(0,1, len(rainfall)), burley(central_molo)[1], label="central molo",scaley=(0,150))
fig.savefig("lower_molo.png")