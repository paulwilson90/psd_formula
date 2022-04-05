from math import cos, sqrt, radians, floor

alt_airport = input("Nominated alternate airport: ")

# WIND SPEED AND DIRECTION
wind_direction = input("Wind direction at 10,000: ")
wind_direction = int(wind_direction)
windspeed = input("Wind speed at 10,000: ")
windspeed = int(windspeed)

# WIND COMPONENT TO CONTINUE TO LHI
track_to_continue = 61  # 061 actual track sydney to lhi
continue_offset = abs(wind_direction - track_to_continue)
continue_rads = radians(continue_offset)
wind_to_continue = round(-(cos(continue_rads) * windspeed))


# TRACKS FROM LHI TO RESPECTIVE ALTERNATE AIRPORT
if alt_airport == 'cfs':
    track_to_divert = 268
    dist_to_alt = 239
    track_diff = 47
    tas = 212
    fuel_flow = 1086
elif alt_airport == 'pmq':
    track_to_divert = 256
    dist_to_alt = 173
    track_diff = 42
    tas = 212
    fuel_flow = 1086
elif alt_airport == 'ntl' or alt_airport == 'wlm':
    track_to_divert = 244
    dist_to_alt = 76
    track_diff = 46
    tas = 212
    fuel_flow = 1086
elif alt_airport == 'tmw':
    track_to_divert = 258
    dist_to_alt = 173
    track_diff = 77  ######### Written as an 83 degree variation in FCOM but it should be 77
    tas = 212
    fuel_flow = 1086
elif alt_airport == 'bne':
    track_to_divert = 293
    dist_to_alt = 407
    track_diff = 56
    tas = 212
    fuel_flow = 1086
elif alt_airport == 'bnk' or alt_airport == 'bna':
    track_to_divert = 284
    dist_to_alt = 330
    track_diff = 50
    tas = 211
    fuel_flow = 1025
elif alt_airport == 'syd':  # trialling sydney for a PSD as it's been discussed in flight many times
    track_to_divert = 360
    dist_to_alt = 0
    track_diff = 0
    tas = 211
    fuel_flow = 1025
else:  # if its YBCG
    track_to_divert = 289
    dist_to_alt = 366
    track_diff = 52
    tas = 211
    fuel_flow = 1025
# WIND COMPONENT TO DIVERT TO ALTERNATE
divert_offset = abs(wind_direction - track_to_divert)
divert_rads = radians(divert_offset)
wind_to_divert = round(-(cos(divert_rads) * windspeed))

wind_divert = int(wind_to_divert)
wind_cont = int(wind_to_continue)

holding_mins = input("Minutes holding required at alternate: ")
fuel_onboard = input("Current fuel onboard: ")
dist_from_syd = input("Current distance from SYD: ")

fuel_adj = ((float(dist_from_syd) / (212 + wind_cont)) * 1086) - 190
fixed_res = 500
holding_fuel = round(int(holding_mins) * 14.1666667)
safe_fuel = int(fuel_onboard) - fixed_res - holding_fuel
ref_fuel = round(((safe_fuel + fuel_adj) / 1000), 2)


if wind_divert == wind_cont:
    psd = ((ref_fuel * 1000) ** 2 - dist_to_alt ** 2 * (fuel_flow / (tas + wind_divert)) ** 2) / (
            2 * (ref_fuel * 1000 * (fuel_flow / (tas + wind_cont)) - dist_to_alt * (fuel_flow / (tas + wind_divert)
                                                                                    ) ** 2 * cos(track_diff / 57.3)))
else:
    psd = (sqrt((2 * (ref_fuel * 1000 * (fuel_flow / (tas + wind_cont)) - dist_to_alt * (fuel_flow / (tas + wind_divert)
                                                                                         ) ** 2 * cos(track_diff / 57.3)
                      )) ** 2 - 4 * ((fuel_flow / (tas + wind_divert)) ** 2 - (fuel_flow / (tas + wind_cont)) ** 2) * (
                        dist_to_alt ** 2 * (fuel_flow / (tas + wind_divert)) ** 2 - (ref_fuel * 1000) ** 2)) - 2 * (
                   ref_fuel * 1000 * (fuel_flow / (tas + wind_cont)) - dist_to_alt * (fuel_flow /
                                                                                      (tas + wind_divert)) ** 2 * cos(
                    track_diff / 57.3))) / 2 / ((fuel_flow / (tas + wind_divert)) ** 2 - (fuel_flow / (tas + wind_cont)
                                                                                          ) ** 2)

print('The point of safe diversion is', str(round(psd)) + 'nm from SYD')
