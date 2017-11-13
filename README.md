## GWSAT Simulation !!!

Here we will simulate the entire lifecycle of the innagural GWSAT.
We'll start with a simple dynamic model and build up to something impressive.
The end goal is to validate the entire mission prior to actual flight, entirely within Python. 

## Environment setup

* Install Anaconda
* Create/Update the `astro` enviornment

~~~
conda env create -f astro.yml
~~~

or

~~~ 
conda-env update -n astro -f astro.yml
~~~

* Run the tests to make sure it's working correctly

~~~
pytest
~~~

* Change environment and run the simulation

~~~
source activate astro
python run_sim.py
~~~

## TODO

* [ ] Orbital dynamics
* [ ] Attitude Dynamics
* [ ] Testing
    * [ ] Make sure all dependencies are working
        * [ ] VTK
        * [ ] Spacetrack
        * [ ] `astro` and `kinematics`

### Things to model

* [ ] High Fidelity gravity model - spherical harmonic
    * [ ] Add to `astro`
* [ ] Earth orientation parameters
    * [ ] Should compare this against SPICE
* [ ] Drag model
* [ ] Star field and star tracker imagery/estimation
* [ ] Ground imaging/pointing - simulate camera imagery of Costa Rica
* [ ] Thruster - muCAT thrusters and all actuators
* [ ] Thermal/Heat 
* [ ] Solar Radiation Pressure and Drag - requires attitude dynamics and a good flat plat model
* [ ] Simulate solar illumination on body for SRP and the ground for imaging
* [ ] Power budget - input from solar panels and output due to components
* [ ] Link budget - simulate ground site transmission/reception
* [ ] Magnetic field of the Earth - one of the primary acutators
* [ ] Simulate GPS constellation - use SPICE/GPS ephemerides
* [ ] Create TraitsUI dialog for starting sim and visualizing multiple
    * [ ] Mayavi animation for orbit
    * [ ] Attitude motion - Body ref frame, ECI, LVLH frames, vectors to sun/ground stations
    * [ ] Camera FOV


