# TDH Lego Truck Big Data Challenge
TDH Lego Truck Big Data Challenge No.3 solution. 

## General Description

## Folder Structure

## Setting up 
The project is organised in four different Docker files. 

In order to run the Batch mode you need to run the `notebooks` container. 

To run Streaming mode you also need to run the Kafka broker, generator+detector and mongodb containers. 

## Running the generator and the detector

Running this container will launch 2 services: a generator service, which loads the data files and streams them into a Kafka topic, and a detector app, which consumes the Kafka topic, enriches the transactions and publishes them as a new Kafka topic. 


```docker-compose up --build```

### Batch Processing
A container was created to run the batch processing. Run it using 

```docker-compose -f docker-compose.jupyter.yml up --build```

This will launch a Jupyter notebook. Navigate and run the notebook `batch.ipynb`.

This notebook contains all the code to load the data and process it according to the instructions. 

#### Assumptions

**Mean acceleration:** calculated using the scalar mean; this does not take into account the direction of the acceleration. Acceleration was computed as the square root of the sum of each of it's axial components sum (sqrt(x^2+y^2+z^2)). 
This was stored in a Pandas dataframe column. 

**Jerk:** based on the previous assumption computed jerk as the delta acceleration over delta time. This were computed for each individual dataset. Three new columns were added (`delta_accel`, `delta_time` and `jerk`).


### Stream Processing 

_Note: This solution was adopted from the code/tutorial found on: 
[Building A Streaming Fraud Detection System With Kafka And Python](https://blog.florimondmanca.com/building-a-streaming-fraud-detection-system-with-kafka-and-python)._ 

## Architecture

![Alt text](/img/tdh_lego_arch.png?raw=true "Solution architecture diagram")

The following commands will launch the containers needed to run the solution. 
1. Create the network 

   ```docker network create kafka-network```
1. Start the Kafka broker

    ```docker-compose -f docker-compose.kafka.yml up --build``` 
2. Start the MongoDB container 

   ```docker-compose -f docker-compose.mongo.yml up --build```
3. Start the generator/detector
  
   ```docker-compose up --build```

The last command will start the generator and detector scripts. The generator will load all files and send messages to the kafka broker, publishing on the `queueing.transactions` topic. The detector will be consuming this topic and enrich each message with break and right turn information. Each procesed message will be inserted in the MongoDB database.

To query the MongoDB database you can use the  notebook in the notebooks docker container: 
   
   ```notebooks/db_query.ipynb```

This notebook will query the db/collection `lego.test` and print all entries.

### Known issues
* The data folder is not shared by both solutions;
* The Mongodb database is not being saved in a local folder (is being recreated each time the container is run).


