#!/usr/bin/env python3

"""Run the main gui to visualize the simualtion
"""

import traitsui.menu
import traits.api
import traitsui.api

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
from mayavi import mlab

from gwsat import visualization, simulation
from astro import constants, geodetic
import numpy as np


# TODO: Do all fo the astrodynamics inside the simulate module instead of here.
# TODO: Leave only GUI shit in this thing
class MainWindow(traits.api.HasTraits):
    run_sim_button = traits.api.Button('Run Sim')
    animate_button = traits.api.Button('Animate')

    # define the Mayavi sceses
    orbit_scene = traits.api.Instance(MlabSceneModel, ())
    groundtrack_scene = traits.api.Instance(MlabSceneModel, ())
    attitude_scene = traits.api.Instance(MlabSceneModel, ())

    # mayavi pipeline elements
    central_body = traits.api.Instance(PipelineBase)
    eci_orbit = traits.api.Instance(PipelineBase)  # orbit in ECI
    eci_sat = traits.api.Instance(PipelineBase)  # satelite position in ECI
    
    groundtrack_image = traits.api.Instance(PipelineBase)
    groundtrack_sat = traits.api.Instance(PipelineBase)
    # arrange the scenes and buttons into groups
    ui_group = traitsui.api.Group(traitsui.api.Item('run_sim_button', style='custom', show_label=False),
                                  traitsui.api.Item(
                                      'animate_button', style='custom', show_label=False),
                                  label='Simulation Control', show_border=True)

    # Orbit/ground track group
    orbit_group = traitsui.api.VSplit(traitsui.api.Item('orbit_scene', editor=SceneEditor(scene_class=MayaviScene),
                                                        label='ECI',
                                                        show_label=False),
                                      traitsui.api.Item('groundtrack_scene', editor=SceneEditor(scene_class=MayaviScene),
                                                        label='Groundtrack',
                                                        show_label=False))
    att_group = traitsui.api.Group(traitsui.api.Item('attitude_scene', editor=SceneEditor(scene_class=MayaviScene),
                                                     label='Attitude',
                                                     show_label=False),
                                   )

    view = traitsui.api.View(traitsui.api.HSplit(ui_group,
                                                 orbit_group,
                                                 att_group),
                             width=800, height=600, resizable=True)

    def _run_sim_button_fired(self):
        """Just run the simulation and save the data
        """
        self.jd, self.state = simulation.run_sim()
         
        # convert ECI state to ECEF and LLA
        self.eci_pos = self.state[:, 0:3]
        self.ecef_pos = np.zeros_like(self.eci_pos)
        self.lla_pos = np.zeros_like(self.eci_pos)
        for ii in range(self.jd.shape[0]):
            Reci2ecef = geodetic.eci2ecef(self.jd[ii])
            ecef = Reci2ecef.dot(self.eci_pos[ii, :])
            self.ecef_pos[ii, :] = ecef
            lla = geodetic.ecef2lla(ecef)
            self.lla_pos[ii, :] = np.array([lla[1], lla[2], lla[3]]) # geodetic


        # draw earth
        self.central_body = visualization.draw_earth(self.orbit_scene)
        # draw the orbit
        self.eci_orbit = visualization.draw_orbit(
            self.state[:, 0:3] / constants.earth.radius, self.orbit_scene)
        
        # draw groundtrack
        self.groundtrack_image = visualization.draw_groundtrack_surface(self.groundtrack_scene)
        self.groundtrack_sat = visualization.draw_groundtrack_sat(self.lla_pos[100, :], self.groundtrack_scene) 

    def _animate_button_fired(self):
        """Animate all the plots
        """
        # initialize ECI orbit plot
        mlab.clf(self.orbit_scene.mayavi_scene)
        self.central_body = visualization.draw_earth(self.orbit_scene)

        # draw the satellite
        pos = self.eci_pos / constants.earth.radius
        self.eci_sat = mlab.points3d(pos[0, 0], pos[0, 1], pos[0, 2], 1,
                                     figure=self.orbit_scene.mayavi_scene,
                                     scale_factor=0.2, color=(1, 0, 0))
        # initialize groundtrack
        mlab.clf(self.groundtrack_scene.mayavi_scene)
        self.groundtrack_image = visualization.draw_groundtrack_surface(self.groundtrack_scene)
        self.groundtrack_sat = visualization.draw_groundtrack_sat(self.lla_pos[100, :], self.groundtrack_scene) 

        # animate all the scenes
        a = visualization.animate_scenes(self.eci_sat.mlab_source, self.groundtrack_sat.mlab_source, pos, self.lla_pos, self.orbit_scene, self.groundtrack_scene)


if __name__ == '__main__':
    MainWindow().configure_traits()
