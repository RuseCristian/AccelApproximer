from logging import error
import numpy as np
from plotly.subplots import make_subplots
from scipy.interpolate import interp1d
import plotly.graph_objects as go
import configparser
import os

initial_speed = 0  # km/h
final_speed = 100

v_init = initial_speed/3.6
v_fin = final_speed/3.6

# car data
config = configparser.ConfigParser()
location = os.path.dirname(os.path.realpath(__file__))+"/data.ini"
config.read(location)

# engine
idle_rpm = int(config['engine']['idle_rpm'])
redline = int(config['engine']['redline'])
rpm = []
torque = []
for key in config['torque_curve']:
    if int(key) <= redline:
        rpm.append(int(key))
        torque.append(int(config['torque_curve'][key]))
        
# gears
gr = []
for element in config['drivetrain_gears']:
    gr.append(float(config['drivetrain_gears'][element]))
    
# drivetrain info
layout = str(config['drivetrain']['layout'])
drivetrain_loss = float(config['drivetrain']['drivetrain_loss'])
shifting_time = float(config['drivetrain']['shifting_time'])
off_clutch = float(config['drivetrain']['off_clutch'])
clutch_bite = float(config['drivetrain']['clutch_bite'])
gas_level = float(config['drivetrain']['gas_level'])
# tire data
tire_width = float(config['tire']['tire_width'])
tire_aspect = float(config['tire']['tire_aspect'])
tire_radial = float(config['tire']['tire_radial'])
tire_mu = float(config['tire']['tire_mu'])
roling_k = float(config['tire']['roling_k'])
# general car data
car_name = str(config['car']['car_name'])
car_mass = float(config['car']['car_mass'])
front_weight_distribution = float(config['car']['front_weight_distribution'])
Cd_car = float(config['car']['Cd_car'])
Frontal_area = float(config['car']['Frontal_area'])
air_density = float(config['car']['air_density'])
number_of_gears = len(gr)-1
lift_coef = float(config['car']['lift_coeficient'])
downforce_total_area = float(config['car']['downforce_total_area'])

# fa o clasa care doar citeste si importeaza fisiere.ini
#

g = 9.81

tire_diameter = (tire_width*tire_aspect*2)/25.4 + tire_radial
# tire diameter in inch

tire_radius = tire_diameter/39.37/2
# tire radius in m

if layout == "Rear":
    max_tractive_force = g*car_mass*(1-front_weight_distribution)*tire_mu
elif layout == "Front":
    max_tractive_force = g*car_mass*front_weight_distribution*tire_mu
# limit of adhestion of tires

hp = np.array([])
rpm = np.array(rpm)
torque = np.array(torque)
max_rpm = rpm[len(rpm)-1]


for i in range(0, len(torque)):
    hp = np.append(hp, int(torque[i]*rpm[i]/7127))
smoother = interp1d(rpm, torque, kind="cubic")
rpm_curve = np.linspace(rpm.min(), rpm.max(), max_rpm)
torque_curve = smoother(rpm_curve)
smoother2 = interp1d(rpm, hp, kind="cubic")
hp_curve = smoother2(rpm_curve)
rpm_curve = np.array(rpm_curve)


# graphs

# torque vs rpm graph
fig = make_subplots(rows=2, cols=3)
fig.add_trace(
    go.Scatter(x=rpm_curve, y=torque_curve,
               name="Torque(Nm)"
               ), row=1, col=1
)

# hp vs rpm graph
fig.add_trace(
    go.Scatter(x=rpm_curve, y=hp_curve,
               name='HP'
               ), row=1, col=1
)


class Gear:
    def __init__(self, accel, rpm, speed):
        self.accel = accel
        self.rpm = rpm
        self.speed = speed


Gears = []
for i in range(0, number_of_gears):

    specific_speed = [(x * tire_diameter)/(gr[i]*gr[len(gr) - 1]
                                           * 336) * 1.609/3.6 for x in rpm_curve]
    # maximum speed at each rpm for specified gear, in m/s

    air_resistance_curve = [
        (Cd_car * Frontal_area * air_density * (x ** 2))/2 for x in specific_speed]
    # air resistance in relation to speed, in Newtons

    downforce_curve = [(lift_coef*downforce_total_area *
                        air_density*(x**2))/2 for x in specific_speed]
    # downforce in relation to speed, in Newtons

    torque_at_the_wheels = [x * gr[i] * gr[len(gr) - 1] for x in torque_curve]
    # torque at the wheels in Nm

    acceleration = []
    for index in range(0, len(torque_curve)-1):

        acceleration_at_specific_rpm = (min(
            (max_tractive_force + downforce_curve[index])*tire_mu, torque_at_the_wheels[index]/tire_radius) - air_resistance_curve[index] - roling_k * g * car_mass)/car_mass
        if acceleration_at_specific_rpm > 0:
            acceleration.append(acceleration_at_specific_rpm)

    g_acceleration = [x/g for x in acceleration]
    acceleration = np.array(acceleration)
    specific_speed = np.array(specific_speed)

    Gear_info = Gear(acceleration, rpm_curve, specific_speed)
    Gears.append(Gear_info)
    # putting together all the info

    specific_speed = [x*3.6 for x in specific_speed]

    fig.add_trace(
        go.Scatter(x=specific_speed, y=torque_at_the_wheels,
                   name="Gear {}".format(i + 1)
                   ), row=2, col=2
    )
    # torque vs speed in each gear (max potential speed)

    fig.add_trace(
        go.Scatter(x=specific_speed, y=g_acceleration,
                   name="Gear {}".format(i + 1)
                   ), row=1, col=2
    )
    # acceleration vs speed graph


# air resistance vs speed graph , in Newtons
fig.add_trace(
    go.Scatter(y=air_resistance_curve, x=specific_speed,
               name="Air resistance (kg)"
               ), row=1, col=3
)
fig.add_trace(
    go.Scatter(y=downforce_curve, x=specific_speed,
               name="Downforce (kg)"
               ), row=2, col=3
)


fig.update_layout(
    title=car_name,
    xaxis_title='RPM',
    yaxis_title='Nm / HP'
)


def find_accel_from_speed(speed, speed_values, accel_values):
    rpm = np.searchsorted(speed_values, speed)
    return accel_values[rpm]


current_v = v_init
current_rpm = -1
current_gear = -1
# finding the gear and rpm to start ,based on the initial speed
try:
    for i in range(0, number_of_gears):
        for x in range(idle_rpm, len(Gears[i].rpm)-1):
            if v_init <= Gears[i].speed[x]:
                current_gear = i
                current_rpm = x
                raise
except:
    pass

if current_rpm < off_clutch and current_gear == 0 and 0 <= initial_speed <= 10:
    delta_rpm = off_clutch - current_rpm
    clutch_progression_rate = abs((clutch_bite - 1))/delta_rpm
    gas_progression_rate = (1 - gas_level)/delta_rpm


# finding the optimum upshift shift points for each gear
optimum_upshift = []
current_gear_accel = 0
next_gear_accel = 0
for i in range(0, number_of_gears-1):
    for x in range(idle_rpm, len(Gears[i].accel)):
        try:
            if Gears[i].accel[x] <= find_accel_from_speed(Gears[i].speed[x], Gears[i+1].speed, Gears[i+1].accel):
                old_x = x
                try:
                    for x in range(x, len(Gears[i].accel)):
                        current_gear_accel += Gears[i].accel[x]
                        next_gear_accel += find_accel_from_speed(
                            Gears[i].speed[x], Gears[i+1].speed, Gears[i+1].accel)
                    if current_gear_accel >= next_gear_accel:
                        optimum_upshift.append(x)
                    else:
                        optimum_upshift.append(old_x)
                    break
                except:
                    if current_gear_accel >= next_gear_accel:
                        optimum_upshift.append(len(Gear[i].accel)-1)
                    else:
                        optimum_upshift.append(old_x)
                    current_gear_accel = 0
                    next_gear_accel = 0
                    pass
                    break

            elif x == len(Gears[i].accel)-1:
                optimum_upshift.append(x)
        except:
            optimum_upshift.append(len(Gears[i].accel)-1)
            break


# calculating max rpm and gear rpm dropdown when upshifting
gear_dropdown_rpm = []
max_speed = []
for i in range(0, number_of_gears):
    try:
        max_speed.append(Gears[i].speed[optimum_upshift[i]])
    except:
        max_speed.append(Gears[i].speed[len(Gears[i].accel)])
        pass


for i in range(0, number_of_gears-1):
    gear_dropdown_rpm.append(np.searchsorted(
        Gears[i+1].speed, Gears[i].speed[optimum_upshift[i]]))


# calculating time needed to reach v_final from v_initial

total_time = 0
while current_v <= v_fin and current_rpm != -1 and current_gear != -1:
    # upshift
    if current_rpm == optimum_upshift[current_gear]:
        total_time += shifting_time
        current_rpm = gear_dropdown_rpm[current_gear]
        current_gear += 1

    # accelerating from standstill in first gear
    if current_gear == 0 and current_rpm < off_clutch and initial_speed == 0 and initial_speed <= 10:
        clutch_bite -= clutch_progression_rate
        gas_level += gas_progression_rate
        total_time = total_time + ((Gears[current_gear].speed[current_rpm] - Gears[current_gear].speed[current_rpm-1])/(
            Gears[current_gear].accel[current_rpm]*(1 - clutch_bite)*gas_level))
        current_v = Gears[current_gear].speed[current_rpm]
        current_rpm += 1
    else:
        # accelerating
        try:
            total_time = total_time + ((Gears[current_gear].speed[current_rpm] -
                                       Gears[current_gear].speed[current_rpm-1])/Gears[current_gear].accel[current_rpm])
            current_v = Gears[current_gear].speed[current_rpm]
        except:
            pass
        current_rpm += 1


total_time = round(total_time, 2)
for i in range(0, number_of_gears):
    print("Gear "+str(i+1)+" Max Speed - " +
          str(round(max_speed[i]*3.6, 2))+" km/h")
    specific_speed = [(x * tire_diameter) /
                      (gr[i]*gr[len(gr) - 1] * 336) * 1.609 for x in rpm_curve]
    fig.add_vline(x=round(max_speed[i-1]*3.6, 2),
                  row=2, col=1, fillcolor="LightSalmon")
    try:
        new_rpm = [x for x in range(0, optimum_upshift[i]+2)]
    except:
        new_rpm = [x for x in range(0, len(Gears[i].accel))]
    fig.add_trace(
        go.Scatter(y=new_rpm, x=specific_speed,
                   name="Gear "+str(i+1)
                   ), row=2, col=1
    )

print("\n")
for i in range(0, number_of_gears-1):
    print("Gear "+str(i+1)+" Optimum Upshift - " +
          str(optimum_upshift[i] + 2) + " RPM")
print("\n")
print(str(initial_speed) + " - "+str(final_speed) +
      " km/h in " + str(total_time) + " seconds")
fig.update_layout(showlegend=False)
fig.show()
input("Press any key to exit.")
