# Python cross-correlation script, using synthetic data
# The max cross correlation coefficient and lag is less accurate when the time series is short.

# Importing modules
import numpy as np
import pylab as pl

#%%

# Creating synthetic data
N = 36001 # Number of samples
Min = 0 
Max = np.pi*100 
Lag = np.pi/4 # Lag between two traces
x = np.linspace(Min,Max,N) 
y1 = np.sin(x/10)*20
r = np.random.randn(N)
y2 = (np.sin((x/10)+Lag)*20)+r

# Providing sample interval and length of time series
Fs = 100 # Hz

t1 = np.linspace(0, len(y1)-1, len(y1))/Fs
t2 = np.linspace(0, len(y2)-1, len(y2))/Fs

# Masking any NAN values
y1m = np.ma.MaskedArray(y1, mask=np.isnan(y1))
y2m = np.ma.MaskedArray(y2, mask=np.isnan(y2))

# Removing offset from arrays
y1or = y1m - np.mean(y1m)
y2or = y2m - np.mean(y2m)

# Normalising arrays
y1n = y1or/max(np.abs(y1or))
y2n = y2or/max(np.abs(y2or))

# Displaying arrays
pl.plot(t1, y1n)
pl.plot(t2, y2n)
pl.show()

# Cross correlating two arrays
cc = np.correlate(y2n,y1n,"full") # Cross-correlating arrays
ac1 = np.correlate(y1n,y1n,"full") # Autocorrelation of first array
ac1mx = max(np.abs(ac1))
ac2 = np.correlate(y2n,y2n,"full") # Autocorrelation of second array
ac2mx = max(np.abs(ac2))
ccn = cc/max(ac1mx, ac2mx) # Cross-correlation coefficients, normalised to between -1 and 1

# Calculating lag between two arrays
tlag = np.linspace(-N+1, N-1, 2*N-1)/Fs
lagofmax = np.argmax(abs(ccn))
tlagofmax = tlag[lagofmax]

# Plotting the data
plcc = pl.plot(tlag,ccn)
pl.ylabel('Correlation Coefficient')
pl.xlabel('Time Lag (seconds)')
linemaxcc = pl.plot((tlagofmax, tlagofmax), (-1, 1), 'k--')
pl.setp(linemaxcc, linewidth=2)

#pl.text(50, 0.5, 'Lag = x')
pl.annotate("Lag = " + str(round(tlagofmax,3)) + "s", xy=(max(tlag)*-1, 0.8))
pl.annotate("Max Corr. Co. = " + str(round(max(abs(ccn)),3)), xy=(max(tlag)*-1, 0.9))
pl.show()



