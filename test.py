import math

def ambient(f_alt):
    h = f_alt*0.3048 # FT to M
    if h < 11000: # TROPOSPHERE
        tempa = 15.04 - 0.00649*h
        press = (101.29 * (((tempa+273.1)/288.08)**5.256))*1000
    elif h < 25000: # LOWER STRATOSPHERE
        tempa = -56.46
        press = (22.65 * math.exp(1.73-0.000157*h))*1000
    else: # SHOULD BE H < 25000
        tempa = 131.21 + 0.00299*h
        press = (2.488 * (((tempa+273.1)/216.6)**(-11.388)))*1000
    
    density = press / (0.2869 * (tempa+273.1))
    tempa_k = tempa + 273.15
    
    return tempa_k, press, density

t,p,d = ambient(40000)
print(t)