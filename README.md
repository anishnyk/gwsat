## GWSAT Simulation !!!

Here we will simulate the entire lifecycle of the innagural GWSAT.
We'll start with a simple dynamic model and build up to something impressive.
The end goal is to validate the entire mission prior to actual flight, entirely within Python. 

## Installation

* Install Anaconda
* Create the environment from the provided file
* Run the tests to ensure it's all setup correctly

## TODO

* [ ] Orbital dynamics
* [ ] Attitude Dynamics

### Things to model

* [ ] High Fidelity gravity model
* [ ] Earth orientation parameters
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



