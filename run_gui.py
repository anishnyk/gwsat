#!/usr/bin/env python3

"""Run the main gui to visualize the simualtion
"""

import traitsui.menu
import traits.api
import traitsui.api

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel

from gwsat import visualization, simulation

class MainWindow(traits.api.HasTraits):
    run_sim_button = traits.api.Button('Run Sim')
    animate_button = traits.api.Button('Animate')
    
    # define the Mayavi sceses
    orbit_scene = traits.api.Instance(MlabSceneModel, ())
    groundtrack_scene = traits.api.Instance(MlabSceneModel, ())
    attitude_scene = traits.api.Instance(MlabSceneModel, ())
    
    # mayavi pipeline elements
    central_body = traits.api.Instance(PipelineBase)

    # arrange the scenes and buttons into groups
    ui_group = traitsui.api.Group(traitsui.api.Item('run_sim_button', style='custom', show_label=False),
                                  traitsui.api.Item('animate_button', style='custom', show_label=False),
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
        jd, state =simulation.run_sim()        
        self.central_body = visualization.draw_earth(self.orbit_scene)         

if __name__ == '__main__':
    MainWindow().configure_traits()

