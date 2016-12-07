import numpy
import matplotlib.pyplot as plt
import random
from crater import Crater

"""Global vars for random 'housekeeping'"""
SURFACE_SIZE = 500
IMPACT_TIME = 1000
PARAM = 1.5
SAT_COUNT = []
SAT_POINT = (0,0)

def createSurface():
    return numpy.zeros((SURFACE_SIZE, SURFACE_SIZE))

def filledSurface(surface, cc, counter):
    """
    Each new impact erases an old impact
    Check if CC is ever greater than 2500, because that is the theoretical limit, given every crater is
    10km, and spaced evenly. (This should almost never happen, but no one likes infinite loops)
    Then, check and see if the last 100 craters are within 1 percent of the first of the 100 craters
    If they are, that means for 100,000 years or 100 impacts the amount of craters has not changed by more than
    1 percent -- Saturated.
    """
    ret = True
    global SAT_POINT
    global SAT_COUNT
    if (cc >= 2500):
        return False
    else:
        if ((counter+1)%100 == 0):
            start = SAT_COUNT[0]
            for x in SAT_COUNT:
                if (start*1.01 >= x):
                    ret = False
                else:
                    SAT_COUNT = []
                    return True
            SAT_POINT = (counter-100, start)
            SAT_COUNT = []
            return ret
        else:
            SAT_COUNT.append(cc)
            return True

def makePlot(surface, year):

    year = str(year*1000)
    fig = plt.figure(figsize=(6, 4))

    ax = fig.add_subplot(111)
    ax.set_title(year)
    plt.imshow(surface, cmap="spectral")
    ax.set_aspect('equal')

    cax = fig.add_axes([0.18, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()

if __name__ == "__main__":
    #Create a surface
    surface = createSurface()

    #Counter = 'years' in thousands
    #craterCounter = amount of craters currently present on the surface
    counter = 0
    craterCounter = 0

    ##cc and y are holders for the plot of craters vs time
    cc = []
    y = []

    charts = []
    percent = []
    cList = []
    while (filledSurface(surface, craterCounter, counter) and (counter < 7000000)):
        counter += 1
        craterSize = (numpy.random.exponential(PARAM) + 1)

        #multiply by 10, because of the Dr = Dc/10 relationship
        craterR, craterC = int(craterSize*10), int(craterSize*10)
        impactR, impactC = random.randint(0,500), random.randint(0,500)

        """This is just to not get an 'index out of bound' error """
        row, col = int((craterR)/2), int((craterC)/2)

        if ((craterR + impactR)/2 > 500):
            row = (500+(craterR+impactR))%500 + 1
        if ((craterC + impactC)/2 > 500):
            col = (500+(craterC+impactC))%500 + 1
        if ((impactR - craterR)/2 < 0):
            row = impactR
        elif((impactC - craterC)/2 < 0):
            col = impactC

        """
        Now for the 'erosion' of adjacent craters from this impact
        """
        ejectaR = int(row*1.5)
        ejectaC = int(col*1.5)

        if ((impactR - ejectaR) < 0):
            ejectaR = impactR
        if ((impactC - ejectaC) < 0):
            ejectaC = impactC
        if ((impactR + ejectaR) > 500):
            ejectaR -= (impactR + ejectaR)%500
        if ((impactC + ejectaC) > 500):
            ejectaC -= (impactR + ejectaR)%500

        """If the ejecta reaches the center of another crater, remove that crater"""
        for crater in cList:
            if ((crater.x < impactR + ejectaR) and (crater.x > impactR - ejectaR) and (crater.y < impactC + ejectaC) and
            (crater.y > impactC - ejectaC)):
                crater.fill(surface)
                cList.remove(crater)
                craterCounter -= 1

        """Now fill the impact zone with 1s"""
        surface[(impactR - row):(impactR + row), (impactC - col):(impactC + col)] = 1
        cList.append(Crater(impactR, impactC, row, col))
        craterCounter += 1
        cc.append(craterCounter)
        y.append(counter*1000)

        charts.append((surface.copy(), counter))


    """This is all plotting stuff, messy, messy, plotting stuff"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(y, cc, lw=0.8)
    ax.plot(SAT_POINT[0]*1000, SAT_POINT[1], marker='o')
    ax = fig.add_subplot(111)
    ax.annotate('Saturation ', xy=(SAT_POINT[0]*1000, SAT_POINT[1]+5), xytext=(SAT_POINT[0]*1000-50, SAT_POINT[1]+30), fontsize=10,
            arrowprops=dict(facecolor='black', shrink=0.005, width=1, headwidth=4),
            )
    ax.set_ylim(0, SAT_POINT[1]+40)
    ax.set_xlim(0, (counter+100)*1000)
    plt.show()
    threes = int(len(charts)/3)
    for i in range(0, len(charts), threes):
        if (i == 0):
            makePlot(charts[10][0], charts[10][1])
        else:
            makePlot(charts[i][0], charts[i][1])
