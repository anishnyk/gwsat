#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

from gwsat import satellite, visualization
import numpy as np
from scipy import integrate
from astro import time, tle

import pdb

start_jd, _ = time.date2jd(2017, 10, 1,0,0,0)
end_jd, _ = time.date2jd(2017, 10, 2, 0, 0, 0)
num_sec = (end_jd - start_jd) * 86400
num_steps = 1e4
t_step = num_sec / num_steps # time step in Julian days

RelTol = 1e-6
AbsTol = 1e-6

sat = satellite.Satellite()

# define the initial state as the ISS
download = False
if download:
    from spacetrack import SpaceTrackClient
    password = input('Enter SpaceTrack password: ')
    st = SpaceTrackClient('shanks.k', password)
    tle = st.tle_latest(norad_cat_id=[25544], format='3le', ordinal=1)
    
    with open('./data/iss.txt', 'w') as f:
        f.write(tle)

sats = tle.get_tle('./data/iss.txt')
iss = sats[0]
# propogate to start JD

iss.tle_update(np.array([start_jd, end_jd]))

# get r,v vectors
initial_pos = iss.r_eci[0, :]
initial_vel = iss.v_eci[0, :]
initial_R = np.eye(3, 3)
initial_w = np.zeros(3)

initial_state = np.concatenate((initial_pos,
                                initial_vel,
                                initial_R.reshape(9),
                                initial_w))

# setup the integrator
system = integrate.ode(sat.eoms_inertial_ode)
system.set_integrator('lsoda', atol=AbsTol, rtol=RelTol, nsteps=num_steps)
system.set_initial_value(initial_state, 0)

jd_sim = np.zeros(int(num_steps + 1))
i_state = np.zeros((int(num_steps + 1), 18))

i_state[0, :] = initial_state
jd_sim[0] = start_jd

ii = 1
while system.successful() and system.t < (num_sec - t_step):
    jd_sim[ii] = (system.t + t_step)*86400 + start_jd
    i_state[ii, :] = system.integrate(system.t + t_step)
    ii += 1

# visualize
visualization.orbit_mayavi(i_state)
