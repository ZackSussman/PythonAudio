import math
 
#oscillators ----------------------------
sin = lambda x: math.sin(x)
#------------------------------------------

def getSignal(duration = 1, frequencyFunction = lambda i: 440, amplitudeFunction = lambda i: 1, sampleRate = 48000, oscillator = sin, *kwargs):
    if "duration" in kwargs:
        duration = kwargs["duration"]
    if "frequencyFunction" in kwargs:
        frequencyFunction = kwargs["frequencyFunction"]
    if "amplitudeFunction" in kwargs:
        amplitudeFunction = kwargs["amplitudeFunction"]
    if "sampleRate" in kwargs:
        sampleRate = kwargs["sampleRate"]
    if "oscillator" in kwargs:
        oscillator = kwargs["oscillator"]
    signal = []
    for i in range(int(duration*sampleRate)):
        signal.append(amplitudeFunction(i)*oscillator((frequencyFunction(i)*2*math.pi)*(i/sampleRate)))
    return clipToEdges(smoothEdges(signal))

def getKick(duration = .1, amplitude = 1, startingPitch = 440, endingPitch = 70, sampleRate = 48000, **kwargs):
    if "duration" in kwargs:
        duration = kwargs["duration"]
    if "startingPitch" in kwargs:
        startingPitch = kwargs["startingPitch"]
    if "amplitude" in kwargs:
        amplitude = kwargs["amplitude"]
    if "endingPitch" in kwargs:
        endingPitch = kwargs["endingPitch"]
    if "sampleRate" in kwargs:
        sampleRate = kwargs["sampleRate"]
    frequencyFunction = lambda i: startingPitch + (endingPitch - startingPitch)*(i/(duration*sampleRate))
    amplitudeFunction = lambda i: amplitude * (1 + - (.7)*(((i)/(duration*sampleRate))**12))
    return getSignal(duration = duration, frequencyFunction = frequencyFunction,  amplitudeFunction = amplitudeFunction)

def normalize(output):
    maxValue = max(output)
    if maxValue == 0: return #prevent division by zero error
    for x in range(len(output)):
        output[x] /= maxValue
    return output

#recursively sum a list of signals that may all be of different lengths
#the algorithm works by summing two signals at a time, then replacing one of the signals in the list with that sum
def sumSignals(signals):
    assert(len(signals) > 0) #can't sum an enpty list!
    if len(signals) == 1: #finished the recursion!
        return signals[0]
    partialSum = []
    shortSig, longSig = signals[0], signals.pop()
    clipToEdges(smoothEdges(shortSig))
    clipToEdges(smoothEdges(longSig))
    if len(longSig) < len(shortSig): shortSig, longSig = longSig, shortSig
    for i in range(len(shortSig)):
        partialSum.append(shortSig[i] + longSig[i])
    for i in range(len(shortSig), len(longSig)):
        partialSum.append(longSig[i])
    signals[0] = partialSum
    return normalize(sumSignals(signals))

#prevent pops------------------------------------------------
def smoothEdges(signal, fadeTime = .05, sampleRate = 48000):
    numSamples = int(fadeTime * sampleRate)
    for i in range(0, numSamples):
        signal[i] *= i/(numSamples - 1)
        signal[-1*i] *= i/(numSamples - 1)
    return signal

def clipToEdges(signal):
    for i in range(len(signal)):
        if signal[i] > 1:
            signal[i] = 1
        elif signal[i] < -1:
            signal[i] = -1
    return signal
#-----------------------------------------------------

def getOvertonedSin(numOvertones, overtoneExponent):
    sinWavList = []
    n = numOvertones
    for x in range(n):
        sinWavList.append(getSinWav(duration = 3, frequencyFunction = lambda i: 440*(2**x), amplitudeFunction = lambda i: (1 - x/(n-1))**overtoneExponent))
    ultimateWav = sumSignals(sinWavList)
    return ultimateWav