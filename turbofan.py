
### THERMODYNAMIC CONSTANTS ###
r = 287

### EFFICIENCIES ###
efficiency_diffuser = 0.97
efficiency_fan = 0.85
efficiency_compressor = 0.85
efficiency_burner = 1.00
efficiency_turbine = 0.97
efficiency_nozzle = 0.98
efficiency_fan_nozzle = 0.97

## GAMMA VALUES ###
gamma_diffuser = 1.40
gamma_fan = 1.40
gamma_compressor = 1.37
gamma_burner = 1.35
gamma_turbine = 1.33
gamma_nozzle = 1.36

### SPECIFIC HEAT CAPACITIES ###
c_p_diffuser = (gamma_diffuser*r)/(gamma_diffuser-1.0)
c_p_fan = (gamma_fan*r)/(gamma_fan-1.0)
c_p_compressor = (gamma_compressor*r)/(gamma_compressor-1.0)
c_p_burner = (gamma_burner*r)/(gamma_burner-1.0)
c_p_turbine = (gamma_turbine*r)/(gamma_turbine-1.0)
c_p_nozzle = (gamma_nozzle*r)/(gamma_nozzle-1.0)

### ENVIRONMENT PARAMETERS ###
flight_altitude = 40000 # FT
flight_mach_number = 0.85
speed_of_sound = 0 
flight_speed = 0

### TURBOFAN PARAMETERS ###
bypass_ratio = 5.00
fan_pressure_ratio = 1.50
compressor_pressure_ratio = 30.00
burner_pressure_ratio = 1.00
turbine_inlet_temperature_maximum = 1700.00
fuel_heating_value = 4.5E7

### STATION VARIABLES ###
temperature_a = 216.7 # ENVIRONMENT DEPENDENT
pressure_a = 18750
temperature_02 = 0
pressure_02  = 0
temperature_03 = 0
pressure_03 = 0
temperature_04 = 1700
pressure_04 = 0
temperature_05 = 0
pressure_05 = 0
temperature_08 = 0
pressure_08 = 0

### FUEL VARIABLES ###
fuel_to_air_ratio = 0
thrust_air_max_flux = 0
thrust_specific_fuel_consumption = 0

### EXIT VARIABLES ###
core_exit_exhaust_velocity = 0
fan_exit_exhaust_velocity = 0

### DIFFUSER ###
def station_02():
    temperature_02 = temperature_a*(1.0 + (((gamma_diffuser - 1.0)/2.0)*(flight_mach_number)**2.0) )
    pressure_02 = pressure_a*((1.0 + (efficiency_diffuser*((temperature_02/temperature_a)-1.0)))**(gamma_diffuser/(gamma_diffuser-1.0)))
    return temperature_02, pressure_02

### FAN ###
def station_08(temperature_02, pressure_02):
    temperature_08 = temperature_02*(1.0 + (1.0/efficiency_fan)*((fan_pressure_ratio**((gamma_fan-1.0)/gamma_fan))-1.0))
    pressure_08 = pressure_02*fan_pressure_ratio
    return temperature_08, pressure_08

### COMPRESSOR ###
def station_03(temperature_02, pressure_02):
    temperature_03 = temperature_02*(1.0 + (1.0/efficiency_compressor)*(((compressor_pressure_ratio)**((gamma_compressor-1.0)/gamma_compressor))-1.0))
    pressure_03 = pressure_02 * compressor_pressure_ratio
    return temperature_03, pressure_03

### BURNER ###
def station_04(temperature_04, pressure_03):
    pressure_04 = pressure_03 * burner_pressure_ratio
    return temperature_04, pressure_04

### TURBINE ###
def station_05(temperature_02, temperature_03, temperature_04, temperature_08, pressure_04, fuel_to_air_ratio):
    temperature_05 = temperature_04 + (1.0/(1.0+fuel_to_air_ratio))*((c_p_compressor/c_p_turbine)*(temperature_02-temperature_03) + bypass_ratio*(c_p_fan/c_p_turbine)*(temperature_02-temperature_08))
    pressure_05 = pressure_04*(1-(1.0/efficiency_turbine)*(1-(temperature_05/temperature_04)))**(gamma_turbine/(gamma_turbine-1.0))
    return temperature_05, pressure_05

def cycle(temperature_04):
    ### DIFFUSER ##
    temperature_02, pressure_02 = station_02()
    ### FAN ###
    temperature_08, pressure_08 = station_08(temperature_02, pressure_02)
    ### COMPRESSOR ###
    temperature_03, pressure_03 = station_03(temperature_02, pressure_02)
    ### BURNER ###
    temperature_04, pressure_04 = station_04(temperature_04, pressure_03)
    ### TURBINE ###
    fuel_to_air_ratio = (temperature_04-temperature_03)/((fuel_heating_value/c_p_burner)-temperature_04)
    temperature_05, pressure_05 = station_05(temperature_02, temperature_03, temperature_04, temperature_08, pressure_04, fuel_to_air_ratio)


    x,y = temperature_05, pressure_05
    print(x,y)

cycle(temperature_04)

