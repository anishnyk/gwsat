"""GWU Satellite module

Extended description of the module

Notes
-----
    This is an example of an indented section. It's like any other section,
    but the body is indented to help it stand out from surrounding text.

If a section is indented, then a section break is created by
resuming unindented text.

Attributes
----------
module_level_variable1 : int
    Descrption of the variable

Author
------
Shankar Kulumani		GWU		skulumani@gwu.edu
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
from astro import propogator, constants
from kinematics import attitude

class Satellite(object):
    """Satellite object
    
    Extended description of the module

    Notes
    -----
        This is an example of an indented section. It's like any other section,
        but the body is indented to help it stand out from surrounding text.
    
    If a section is indented, then a section break is created by
    resuming unindented text.
    
    Attributes
    ----------
    module_level_variable1 : int
        Descrption of the variable

    Author
    ------
    Shankar Kulumani		GWU		skulumani@gwu.edu
    """

    def __init__(self):
        r"""Initialize the satellite and it's properties

        Extended description of the function.

        Author
        ------
        Shankar Kulumani		GWU		skulumani@gwu.edu

        """ 

        self.m = 3.5 # kilogram
        self.J = np.diag([1, 1, 1]) # moment of inertia

    def eoms_inertial_ode(self, t, state):
        """
        EOMS of spacecraft with respect to Earth in the ECI frame
        """
        
        pos = state[0:3]
        vel = state[3:6]
        R = np.reshape(state[6:15], (3,3)) # rotation from body frame to ECI
        w = state[15:18] # ang vel of body frame wrt ECI in body frame

        m_sat = self.m
        J = self.J
        accel_gravity = propogator.accel_twobody(m_sat, constants.earth.mass, pos, constants.G)
        ext_moment = np.zeros(3)
        
        pos_dot = vel
        vel_dot = accel_gravity
        R_dot = R.dot(attitude.hat_map(w))
        w_dot = np.linalg.inv(J).dot(ext_moment - attitude.hat_map(w).dot(J).dot(w))

        state_dot = np.concatenate((pos_dot, vel_dot, R_dot.reshape(9), w_dot))
        return state_dot

