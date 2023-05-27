import matplotlib.pyplot as plt
import numpy as np

# 100 linearly spaced numbers
max_x_value = 200000
x = np.linspace(1,max_x_value,200000)

# considered cars
types = {'BEV','PHEV'}
seasons = {'summer','winter'}

# mCO2_Vehicle in kg
mCO2_Vehicle = {
    'BEV': 4000,
    'PHEV': 4500,
}

# production CO2 emissions per kWh 
f_prod_bat = 127

# Capacity of batteries in kWh
W_bat = {
    'BEV': 53,
    'PHEV': 12,
}

# mCO2_Battery in kg
mCO2_Battery = {}
for type in types:
    mCO2_Battery[type] = f_prod_bat * W_bat[type]
    
# Relative CO2 emissions for energy carrier production in kg/kWh
emissions_energy_carrier_production = {
    'summer': 379 * 10 **-3,
    'winter': 379 * 10 **-3
}

# vehicle electrical energy consumption in kWh / km
electric_consumption = {
    'BEV': 14.3 / 100,
    'PHEV': 15 / 100
}

# vehicle fuel consumption in L / km
fuel_consumption = {
    'BEV': 0 / 100, 
    'PHEV': 1.6 / 100
}

# Relative CO2 emissions for fuel production in kg / L
emissions_fuel_production = 600 * 10**-3

# Tailpipe emissions in kg / L
emissions_tailpipe = 2370 * 10**-3

# mCO2_Operation in kg/km
mCO2_Operation = {}
for type in types:
    mCO2_Operation[type] = 0  # Initialize the key with a value of 0
    for season in seasons:
        mCO2_Operation[type] += electric_consumption[type] * emissions_energy_carrier_production[season] / 2

    if type == 'PHEV':
        mCO2_Operation[type] += (fuel_consumption[type] * (emissions_fuel_production + emissions_tailpipe))


mCO2_Recycling = {
    'BEV': 0,
    'PHEV': 0,
}


# the function
mCO2_total = {}
for type in types:
    mCO2_total[type] = mCO2_Vehicle[type] + mCO2_Battery[type] + mCO2_Operation[type] * x + mCO2_Recycling[type]

print("mCO2_Vehicle:", mCO2_Vehicle)
print("mCO2_Battery:", mCO2_Battery)
print("mCO2_Operation:", mCO2_Operation)
print("mCO2_Recycling:", mCO2_Recycling)
print("mCO2_total_BEV", mCO2_total['BEV'][x == 180000])
print("mCO2_total_PHEV", mCO2_total['PHEV'][x == 180000])

# setting the axes at the centre
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Mileage [km]')
ax.set_ylabel('CO2-emissions [kg]')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Additional adjustments to the y-axis
max_y = np.max(np.maximum(mCO2_total['BEV'][x == max_x_value], mCO2_total['PHEV'][x == max_x_value]))
ax.set_ylim(0, max_y + 1000)  # Set the y-axis limits

# Additional adjustments to the x-axis
ax.spines['bottom'].set_bounds(0, max_x_value)  # Set the x-axis bounds
ax.set_xlim(0, max_x_value)  # Set the x-axis limits

# plot the functions
plt.plot(x,mCO2_total['BEV'], 'b', label='BEV')
plt.plot(x,mCO2_total['PHEV'], 'r', label='PHEV')


plt.legend(loc='upper left')

# show the plot
plt.show()
