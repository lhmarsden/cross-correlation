# Python cross-correlation script
# The script reads in files of single events. Each file should contain only one column 
# (the amplitude of each sample), or the script should be modified to account for this.
# A cross correlation matrix is produced for all the events loaded, with the event time
# of each event plotted on the x and y axis, and the maximum cross correlation coefficient between
# any two events plotted in colour between -1 and 1.
# The max cross correlation coefficient and lag is less accurate when the time series is short.
# Offset should have been removed from each event prior to running this script

# Importing modules
import numpy as np
import pylab as pl
import os
import datetime

#%%
# Setting values
Fs = 100 # Hz, sample frequency
l = 2000 # length in number of samples
lt = l/Fs # length of each event in seconds

# Loading files, which are clipped to one event per file.
# Search for events, append name of each file to array
eventlist = []
for files in os.listdir('/nfs/a136/eelhm/eventcount/'):
    if 'event.RETU.SHZ.' in files:
        eventlist.append(files)
#%%
# Sort list in temporal order
eventlist = sorted(eventlist)

# Initialising values
e1_time = [] # Time of first events
e1_count = [] # First events sequentially numbered 
e2_time = [] # Time of second events
e2_count = [] # Second events sequentially numbered 
max_corr_co = [] # Max normalised correlation coefficient between any two events
event_time = [] # Time of each event (array of strings, for plot)
e1c = 0 # Counter for loop
corrgrid = np.zeros(shape=(25,25)) # Initialising grid to store cross correlation coefficient of each pair of events



for e1 in eventlist: # Loop through each event
    #Taking the parameters below from the file name
    e1_split = e1.split(".")
    e1_year = int(e1_split[3])
    e1_month = int(e1_split[4])
    e1_dayinmonth = int(e1_split[5])
    e1_hour = int(e1_split[6])
    e1_minute = int(e1_split[7])
    e1_second = int(e1_split[8])
    e1dt = datetime.datetime(e1_year, e1_month, e1_dayinmonth, e1_hour, e1_minute, e1_second) # Datetime of each event
    e1ut = int(e1dt.strftime('%s')) # Datetime of event as integer, for file name

    f1 = open('/nfs/a136/eelhm/eventcount/' + e1, 'r')
    e1d = np.genfromtxt(f1, delimiter=',') # Creating array of event
    e1rn = e1d
    blanks = np.isnan(e1d)
    e1rn[blanks] = 0 # Replacing NaN values with 0s to make following steps work
    e1n = e1rn/max(np.abs(e1rn)) # Normalising event to between -1 and 1

    e1c = e1c + 1
    e2c = 0

    event_time.append("%02d" % (e1_hour) + ":" + "%02d" % (e1_minute) + ":" + "%02d" % (e1_second))

    for e2 in eventlist: # Loop through 2nd event to correlate with first
        #Taking the parameters below from the file name
        e2_split = e2.split(".")
        e2_year = int(e2_split[3])
        e2_month = int(e2_split[4])
        e2_dayinmonth = int(e2_split[5])
        e2_hour = int(e2_split[6])
        e2_minute = int(e2_split[7])
        e2_second = int(e2_split[8])
        e2dt = datetime.datetime(e2_year, e2_month, e2_dayinmonth, e2_hour, e2_minute, e2_second) # Datetime of each event
        e2ut = int(e2dt.strftime('%s')) # Datetime of event as integer, for file name

        f2 = open('/nfs/a136/eelhm/eventcount/' + e2, 'r') # Loading event 
        e2d = np.genfromtxt(f2, delimiter=',') # Creating array of event
        e2rn = e2d
        blanks = np.isnan(e2d)
        e2rn[blanks] = 0 # Replacing NaN values with 0s to make following steps work
        e2n = e2rn/max(np.abs(e2rn)) # Normalising event
        
        # Performing cross-correlation of two events
        cc = np.correlate(e2n,e1n,"full") # cross correlation coefficients
        ac1 = np.correlate(e1n,e1n,"full") # Autocorrelation of first event
        ac1mx = max(np.abs(ac1))
        ac2 = np.correlate(e2n,e2n,"full") # Autocorrelation of second event
        ac2mx = max(np.abs(ac2))
        ccn = cc/max(ac1mx, ac2mx) # Normalising cross correlation coefficients to between -1 and 1
        ccmax = max(ccn, key=abs)  # Maximum correlation coefficient for pair of events

        # Appending values to array
        e1_time.append(e1ut)
        e2_time.append(e2ut)
        max_corr_co.append(ccmax)
        e2c = e2c + 1
        e1_count.append(e1c)
        e2_count.append(e2c)
        corrgrid[(e1c-1), (e2c-1)] = ccmax # Storing max cross correlation coefficent between for pair of events to location in grid


# Plot count on x and y axis as heatmap
pl.matshow(corrgrid, cmap=pl.cm.RdBu)
x_pos = np.arange(len(event_time))
pl.xticks(x_pos, event_time)
pl.xticks(x_pos,rotation=90)
y_pos = np.arange(len(event_time))
pl.yticks(y_pos, event_time)
pl.clim(-1, 1)
pl.colorbar()
pl.show()


        

