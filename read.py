import pickle
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button

raw_output = open(sys.argv[1],'rb')
loaded_output =  pickle.load(raw_output)

time_calibration = loaded_output['time'][0]

#global alpha 
alpha = 1
#global normalized_array
normalized_array = []
normalFactor = 0

def normalize(src):
	dst = []
        for i in range(len(src)):
		if i==0:
			dst.append(src[i])
			continue
		dst.append(dst[i-1] + alpha*(src[i] - dst[i-1]))
        return dst
		
def fill_normalized():
    for i in range(100):
        if i == 0:
            normalized_array.append(loaded_output['ay'])
            continue
        normalized_array.append(normalize(normalized_array[i-1]))

def trapezoidalSum(x,y):
    approximation = []
    rollingSum = 0
    for i in range(len(x)-1):
        rollingSum+=(x[i+1] - x[i]) * (y[i+1] + y[i]) * 0.5 
        approximation.append(rollingSum)
    approximation.append(rollingSum)
    return approximation

#normalize(loaded_output['ay'],normalized_ay)
#normalize(normalized_ay,double_normalized_ay)
#normalize(double_normalized_ay,triple_normalized_ay)
#normalize(triple_normalized_ay, quadruple_normalized_ay)

fill_normalized()

fig = plt.figure()

ax1 = fig.add_subplot(211)
#ax1.set_ylim(-10,10)
ax1.plot(np.array(loaded_output['time'])-time_calibration,trapezoidalSum(loaded_output['time'],trapezoidalSum(loaded_output['time'],loaded_output['ay'])),color='navy')
ax1Pos = ax1.get_position()
ax1NewPos = [ax1Pos.x0,ax1Pos.y0+0.1,ax1Pos.width,ax1Pos.height]
ax1.set_position(ax1NewPos)


ax2 = fig.add_subplot(212)
#ax2.set_ylim(-10,10)
ax2.plot(np.array(loaded_output['time'])-time_calibration,normalized_array[normalFactor],color='navy')
ax2Pos = ax2.get_position()
ax2NewPos = [ax2Pos.x0,ax2Pos.y0+0.1,ax2Pos.width,ax2Pos.height]
ax2.set_position(ax2NewPos)

def change_alpha(newAlpha):
    global alpha
    global normalized_array
    del(normalized_array)
    normalized_array = []
    alpha = newAlpha
    fill_normalized()
    redrawAx2()

def redrawAx2():
    global buttonText
    ax2.lines[0].remove()
    ax2.plot(np.array(loaded_output['time'])-time_calibration,normalized_array[normalFactor],color='navy')
    ax1.lines[0].remove()
    ax1.plot(np.array(loaded_output['time'])-time_calibration,trapezoidalSum(loaded_output['time'],trapezoidalSum(loaded_output['time'],normalized_array[normalFactor])),color='navy') 
    
    buttonText.set_text(normalFactor)
    fig.canvas.draw()

def incrementNormalFactor(x):
    global normalFactor
    normalFactor+=1
    redrawAx2()

def decrementNormalFactor(x):
    global normalFactor
    normalFactor-=1
    redrawAx2()

alphaSlider = Slider(plt.axes([0.1,0.1,0.25,0.02]),'Alpha',0,1,valinit=1)
alphaSlider.on_changed(change_alpha)

decButton = Button(plt.axes([0.1,0.03,0.03,0.03]),'-')
incButton = Button(plt.axes([0.2,0.03,0.03,0.03]),'+')
decButton.on_clicked(decrementNormalFactor)
incButton.on_clicked(incrementNormalFactor)
buttonText = plt.text(-1.5,0.5,normalFactor)

plt.show()


