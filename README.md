# tdh_lego
TDH Lego Truck Challenge


## Folder Structure

## Setting up 

The project is organised in two different Docker files. 

In order to run the Batch mode you need to run the generator+detector docker containers. 

To run Streaming mode you also need to run the Kafka broker. 

## Running

### Batch Processing
The script to process all data in batch mode can be found in the `generator/notebooks/batch.ipynb` notebook.


#### Assumptions

**Mean acceleration:** calculated using the scalar mean; this does not take into account the direction of the acceleration. Acceleration was computed as the square root of the sum of each of it's axial components sum (sqrt(x^2+y^2+z^2)). 
This was stored in a Pandas dataframe column. 

**Jerk:** based on the previous assumption computed jerk as the delta acceleration over delta time. This were computed for each individual dataset. Three new columns were added (`delta_accel`, `delta_time` and `jerk`).


### Stream Processing 

### Todo


