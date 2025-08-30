import numpy
import matplotlib.pyplot as plt
import pandas

class Watershed:
    def __init__(mean, spread, size):
        self.mean = mean
        self.spread = spread
        self.size = size

# running the model amounts to computing the flow in each watershed on each day.

# in this version the rain which falls just flushes through the system straight away.

rainfall     = numpy.array([11.4,0,0.4,0,0,2,0.2,0.2,0.2,0,0,8.3,2.1])

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

systems = [upper_molo, googong, lower_quean, jerra, central_molo, lower_molo]
table = pandas.DataFrame(systems, index=["upper_molo", "googong", "lower_quean", "jerra", "central_molo", "lower_molo"])
rainfall_table = pandas.DataFrame([rainfall], index=["rainfall"])

print("This system assumes that the rainfall all over the river system is the same and can be described with one number per day.")
print("Rainfall (mm) per day:")
print(rainfall_table)
print("")
print("Running the model computes the flow in each watershed on each day. (in L/second)")
print(table)

fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(numpy.linspace(0,1, len(rainfall)), lower_molo, label="lower molo", scaley=(0,150))
ax1.plot(numpy.linspace(0,1, len(rainfall)), central_molo, label="central molo",scaley=(0,150))
ax2.plot(numpy.linspace(0,1, len(rainfall)), burley(central_molo)[1], label="central molo",scaley=(0,150))
fig.savefig("lower_molo.png")