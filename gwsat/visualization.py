"""Visualization functions for the orbit/attitude

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

from mayavi import mlab
from mayavi.sources.builtin_surface import BuiltinSurface
import numpy as np
from astro import constants

def draw_earth(scene):
    continents_src = BuiltinSurface(source='earth', name='Continents')
    continents_src.data_source.on_ratio = 2
    continents = mlab.pipeline.surface(continents_src, color=(0, 0, 0),
                                       figure=scene)
    sphere = mlab.points3d(0, 0, 0, 1, scale_mode='none', scale_factor=2,
                           color=(0.67, 0.77, 0.93), resolution=10,
                           opacity=0.9, name='Earth',
                           figure=scene)
    sphere.actor.property.specular = 0.45
    sphere.actor.property.specular_power = 5
    sphere.actor.property.backface_culling = True

    # draw the axes
    scale = 5
    line_width = 5
    mode = '2ddash'
    xaxis = mlab.quiver3d(0, 0, 0, 1, 0, 0,
                          scale_mode='vector', scale_factor=scale, color=(1, 0, 0),
                          line_width=line_width, mode=mode,
                          figure=scene)
    yaxis = mlab.quiver3d(0, 0, 0, 0, 1, 0,
                          scale_mode='none', scale_factor=scale, color=(0, 1, 0),
                          line_width=line_width, mode=mode,
                          figure=scene)
    zaxis = mlab.quiver3d(0, 0, 0, 0, 0, 1,
                          scale_mode='none', scale_factor=scale, color=(0, 0, 1),
                          line_width=line_width, mode=mode,
                          figure=scene)

    x, y = np.mgrid[-10:10, -10:10]
    plane = mlab.surf(x, y, np.zeros_like(x), opacity=0.1,
                      extent=[-10, 10, -10, 10, 0, 0],
                      figure=scene)

    return sphere

def draw_orbit(pos_eci, scene):
    """
    Inputs are scaled according to radius of central body
    """
    line_width = 10
    tube_radius = 0.05
    orbit = mlab.plot3d(pos_eci[:, 0], pos_eci[:, 1], pos_eci[:, 2],
                        np.ones_like(pos_eci[:, 0]),
                        line_width=line_width, tube_radius=tube_radius,
                        color=(1, 0, 0),
                        figure=scene)
    return orbit

def draw_sat(sat_eci, scene):
    """
    Scaled by body radius
    """
    sat = mlab.points3d(sat_eci[0], sat_eci[1], sat_eci[2], 1,
                        scale_factor=0.5, scale_mode='none',
                        color=(0, 0, 0),
                        figure=scene)
    return sat

def orbit_mayavi(inertial_state):
    pos_eci = inertial_state[:, 0:3]
    scene = mlab.figure()
    sphere = draw_earth(scene)
    orbit = draw_orbit(pos_eci / constants.earth.radius, scene)
    
    mlab.show()
