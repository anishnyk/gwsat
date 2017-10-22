"""Test to make sure everything is installed properly

"""

import numpy as np
from mayavi import version
import vtk
from astro import time
from kinematics import attitude
import spiceypy as spice
import spacetrack 

def test_mayavi_version():
    version_actual = version.version
    np.testing.assert_string_equal(version_actual, '4.5.0')
