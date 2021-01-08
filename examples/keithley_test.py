#!/usr/bin/env python

VOLTAGE_INDEX = 0;
CURRENT_INDEX = 1;

### KEITHLEY COMMANDS - THESE ACTUALLY WORK.
# Apply a bunch of voltages, and get back the I/V curve 
# Gives back a numpy array of voltages and currents [v, c]
def getIVDataVoltage(device, voltages):
    voltages = np.array(voltages);
    currents = np.array([]);
    for v in voltages:
        currents = np.append(currents, getIData(device, v));
    device.write('source:clear:immediate')
    return np.array([voltages,currents])

# Apply a voltage, and get the current that results
def getIData(device, voltage):
    device.write("source:function:voltage");
    device.write("configure:current");
    device.write('source:voltage:level ' + str(voltage));
    data = device.query('read?')
    split_data = data.split(',');
    numerical_data = list(map(float, split_data));
    return numerical_data[CURRENT_INDEX];

# Apply a voltage, and get the current that results
def getVData(device, current):
    device.write("source:function:current"); # Configure the Source to apply current
    device.write("configure:voltage"); # Configure the measurement unit to measure voltage
    device.write('source:current:level ' + str(current));
    # device.write('output on'); # Turn on the source. Not sure if necessary.
    data = device.query('read?')
    split_data = data.split(',');
    numerical_data = list(map(float, split_data));
    return numerical_data[CURRENT_INDEX];


print(keithley.write('configure:voltage'))
print(keithley.write('source:current:level 0.00005'))


# First, plug in the thing and go to the MATLAB instrument test and 
# measurement and scan for changes. Then run this. You should see a 
# resource come up with 'GPIB0::XX::INSTR' or something.
import visa
import time
import numpy as np
import matplotlib.pyplot as plt

rm = visa.ResourceManager();

# Next, you can open the resource using rm.open_resource();
keithley = rm.open_resource("GPIB0::24::INSTR")
keithley.read_termination = '\n';
keithley.write_termination= '\n';
# Now, define a bunch of functions that we can use to read voltages and 
# currents


# In[179]:





# In[339]:


voltages = np.arange(-1,1,0.001)
data = getIVDataVoltage(keithley, voltages)
plt.plot(data[0],data[1])
plt.show()
# This is the data for a resistor


# In[365]:


# Measured data for largest single device with fat contacts
pvoltages = np.arange(-1.5,1.5,0.01)
p_16u_data = getIVDataVoltage(keithley, pvoltages)
plt.plot(p_16u_data[0],p_16u_data[1])
plt.show()


# In[366]:


# Measured data for largest single device with fat contacts
pvoltages = np.arange(-2,2,0.01)
p_16u_data = getIVDataVoltage(keithley, pvoltages)
plt.plot(p_16u_data[0],p_16u_data[1])
plt.show()


# In[369]:


# Measured data for largest single device with fat contacts
pvoltages = np.arange(-3,3,0.01)
p_16u_data = getIVDataVoltage(keithley, pvoltages)
plt.plot(p_16u_data[0],p_16u_data[1])
plt.show()


# In[370]:


# Measured data for single device #2
voltages = np.arange(-3,3,0.01)
dev2_data = getIVDataVoltage(keithley, voltages)
plt.plot(dev2_data[0],dev2_data[1])
plt.show()


# In[289]:


np.transpose(data)


# In[337]:


np.arange(0,1,0.1)


# In[ ]:


# MISCELLANEOUS NOTES
# We want to get some information about the system. We can do this
# by asking for its identifier.
keithley.query('*IDN?')

# There are two ways to do this - the first is to use a single query
# command, which writes and then reads. The second is to explicitly
# write a command and then read out the data buffer.
#keithley.write('*IDN?')
#while True:
#    print(keithley.read_bytes(1))

# first, reset the equipment
print(keithley.write("*RST"))

# now, set the current and voltage ranges to what we want
print(keithley.write("configure:current"))

# Now, apply a voltage. I have no idea how to do this.

# Now, reconfigure the device to record voltage instead of current
# print(keithley.write("configure:voltage"))

# Now that we have configured out device to measure current, 
# we want to set up the voltage source. We do this through the 
# 'source' commands. 

# Sets the voltage source to a value of 2V
keithley.write('source:voltage:level 0.5')

# However, now we still need to turn on the voltage source. 

# Now, read some data
print(keithley.query("read?"))

# This is equivalent to this:
print(keithley.write('initiate'))
print(keithley.query('fetch?'))


# So it looks like the "fetch" query command grabs the latest
# post-processed data (I assume that means filtered data)
# Now the question is, what are these five numbers it gives me?
# One of them may be time.

# Apparently executing fetch actually does nothing to the sample buffer.
# So executing fetch multiple times will yield the same data, as I have
# seen. It also looks like fetch will grab all the data, which they
# claim is voltage, current, resistance, timestamp, and status. Not sure
# which of these numbers is which. 

# Now, read some (new) data. This apparently does an initiate 
# followed by a fetch. The initiate performs a new measurement cycle,
# and fetch grabs that.

# I believe the data block is Voltage, Current, Resistance (?), 
# Time, Status(?).

# We can also get statistics with calculate3, but it's not clear how to
# do this. 

# Here, we can set the filter to be a moving average
print(keithley.write('sense:average:tcontrol moving'))

# With a moving average sample count of 100
print(keithley.write('sense:average:count 10'))

# Now, we just need to figure out how to 

# Turn off the voltage source 
# keithley.write('source:clear:immediate')

# Now, we just need to figure out how to adjust the voltage/current limit.
# This is how it is done.
# print(keithley.write('sense:current:protection:level 0.0005'))


# In[380]:


# Measured data for bare Al/Si to Si contacts. The
# voltage applied is with respect to the smaller pad. This means positive voltages
voltages = np.arange(-1,1,0.001)
bare_data = getIVDataVoltage(keithley, voltages)
plt.plot(bare_data[0],bare_data[1])
plt.show()


# In[381]:


# Measured data for bare Al/Si to Si contacts. The
# voltage applied is with respect to our large (ground) pad.
# This data is for 
voltages = np.arange(-1,1,0.01)
data_small_capacitor = getIVDataVoltage(keithley, voltages)
plt.plot(bare_data[0],bare_data[1])
plt.show()


# In[384]:


data_med_capacitor = getIVDataVoltage(keithley, voltages)
plt.plot(data_med_capacitor[0],data_med_capacitor[1])
plt.show()


# In[385]:


data_big_capacitor = getIVDataVoltage(keithley, voltages)
plt.plot(data_big_capacitor[0],data_big_capacitor[1])
plt.show()


# In[387]:


voltages_extended = np.arange(-3,3,0.01)
data_big_capacitor_extended = getIVDataVoltage(keithley, voltages_extended)
plt.plot(data_big_capacitor_extended[0],data_big_capacitor_extended[1])
plt.show()


# In[417]:


area_ground_plane = (0.44*2+0.66*2)*0.05
area_big_capacitor = 0.1*0.1 #area in square centimeters
area_med_capacitor = 0.04*0.04;
area_small_capacitor = 0.01*0.01;
Jreverse = data_big_capacitor[1,-1]/area_big_capacitor; # Maximum reverse saturation current density


# In[393]:


test_arr = np.arange(0,1,0.1)


# In[402]:


print(data_big_capacitor[1,-1]/area_big_capacitor)
print(data_med_capacitor[1,-1]/area_med_capacitor)
print(data_small_capacitor[1,-1]/area_small_capacitor)


# In[413]:


print((data_big_capacitor[0,-1]-data_big_capacitor[0,-70])/(data_big_capacitor[1,-1]-data_big_capacitor[1,-70])*area_big_capacitor)
