import matplotlib.pyplot as plt
import numpy as np

# 100 linearly spaced numbers
max_x_value = 500000
x = np.linspace(1,max_x_value,200000)

# considered cars
types = {'BEV','PHEV'}
seasons = {'summer','winter'}
energy_carrier_production = {'Germany 2050'}#'Germany 2022','Germany 2030','Germany 2050','Photovoltaik 2021','Wind Onshore 2021','Wind Offshore 2021'}

# mCO2_Vehicle in kg
mCO2_Vehicle = {
    'BEV': 19200,
    'PHEV': 10100,
}

# production CO2 emissions per kWh 
f_prod_bat = 109.27

# Capacity of batteries in kWh
W_bat = {
    'BEV': 64,
    'PHEV': 6.38,
}

# mCO2_Battery in kg
mCO2_Battery = {}
for type in types:
    mCO2_Battery[type] = f_prod_bat * W_bat[type]
    
# Relative CO2 emissions for energy carrier production in kg/kWh (electric energy)
emissions_energy_carrier_production = {
    'Germany 2022': 434 * 10**-3,
    'Germany 2030': 376 * 10**-3,
    'Germany 2050': 233 * 10**-3,
    'Photovoltaik 2021': 56.550 * 10**-3,
    'Wind Onshore 2021': 17.693 * 10**-3,
    'Wind Offshore 2021': 9.664 * 10**-3,
}

# vehicle electrical energy consumption in kWh / km
electric_consumption = {
    'BEV': 0.198 ,
    'PHEV': 0.11 
}

# vehicle fuel consumption in L / km
fuel_consumption = {
    'BEV': 0 / 100, 
    'PHEV': 2.1 / 100
}

# Relative CO2 emissions for fuel production in kg / L (PHEV only)
emissions_fuel_production = {
    'gasoline from petroleum':	544 * 10**-3,
    'e-fuel': 740 * 10**-3
}

# Tailpipe emissions in kg / L (PHEV only)
emissions_tailpipe = 2280 * 10**-3

# mCO2_Operation in kg/km
mCO2_Operation = {}
for type in types:
    mCO2_Operation[type] = {}  # Initialize the key with a value of 0
    for i in energy_carrier_production:
        mCO2_Operation[type][i] = electric_consumption[type] * emissions_energy_carrier_production[i]

        if type == 'PHEV':
            mCO2_Operation[type][i] += (fuel_consumption[type] * (emissions_fuel_production['e-fuel'] + emissions_tailpipe))


mCO2_Recycling = {
    'BEV': 500,
    'PHEV': 400,
}


# the function
mCO2_total = {}
for type in types:
    mCO2_total[type] = {}
    for i in energy_carrier_production:
        mCO2_total[type][i] = mCO2_Vehicle[type] + mCO2_Battery[type] + mCO2_Operation[type][i] * x + mCO2_Recycling[type]

print("mCO2_Vehicle:", mCO2_Vehicle)
print("mCO2_Battery:", mCO2_Battery)
print("mCO2_Operation:", mCO2_Operation)
print("mCO2_Recycling:", mCO2_Recycling)
# print("mCO2_total_BEV", mCO2_total['BEV'][x == 180000])
# print("mCO2_total_PHEV", mCO2_total['PHEV'][x == 180000])

# setting the axes at the centre
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Mileage [km]')
ax.set_ylabel('CO2-emissions [kg]')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Additional adjustments to the y-axis
# max_y = np.max(np.maximum(list(mCO2_total['BEV'].values()), list(mCO2_total['PHEV'].values())))
max_y = 50000
ax.set_ylim(0, max_y + 1000)  # Set the y-axis limits

# Additional adjustments to the x-axis
ax.spines['bottom'].set_bounds(0, max_x_value)  # Set the x-axis bounds
ax.set_xlim(0, max_x_value)  # Set the x-axis limits

# plot the functions
for i in energy_carrier_production:
    plt.plot(x,mCO2_total['BEV'][i], color = 'tab:orange', label='BEV '+i)
    plt.plot(x,mCO2_total['PHEV'][i], color = 'tab:blue', label='PHEV '+i)


# Find the intersection point
intersection = np.where(np.isclose(mCO2_total['BEV'][i], mCO2_total['PHEV'][i]))[0]
print(intersection)
if len(intersection) > 0:
    intersection_point = (x[intersection[0]], mCO2_total['BEV'][i][intersection[0]])
    intersection_text = f"Breakeven point at x={round(intersection_point[0],-2)}km"
else:
    print("No intersection point found.")

# Plot the intersection point
plt.title(intersection_text)

plt.legend(loc='upper left')

# show the plot
plt.show()