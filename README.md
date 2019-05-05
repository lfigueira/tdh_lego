# TDH Lego Truck Big Data Challenge
TDH Lego Truck Big Data Challenge No.3 solution. 

[![Python](https://img.shields.io/badge/python-3.5+-blue.svg?style=flat-square)](https://www.python.org)
[![Kafka](https://img.shields.io/badge/streaming_platform-kafka-black.svg?style=flat-square)](https://kafka.apache.org)
[![Docker Images](https://img.shields.io/badge/docker_images-confluent-orange.svg?style=flat-square)](https://github.com/confluentinc/cp-docker-images)


## General Description

## Folder Structure

## Setting up 

The project is organised in two different Docker files. 

In order to run the Batch mode you need to run the generator+detector docker containers. 

To run Streaming mode you also need to run the Kafka broker. 

## Create network
If running the stream section you need to add a docker network: 

```docker network create kafka-network```

## Running the Kafka broker

```docker-compose -f docker-compose.kafka.yml up```


## Running the generator and the detector

Running this container will launch 2 services: a generator service, which loads the data files and streams them into a Kafka topic, and a detector app, which consumes the Kafka topic, enriches the transactions and publishes them as a new Kafka topic. 

Launching this container will automatically start a Jupyter notebook on localhost, port 8888 (see console for details). 

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

This solution was adopted from the code/tutorial found on: 
[Building A Streaming Fraud Detection System With Kafka And Python](https://blog.florimondmanca.com/building-a-streaming-fraud-detection-system-with-kafka-and-python).

  1. Start the broker
  2. Start the generator/detector

 ```docker-compose up --build```

## Architecture

![Alt text](/img/tdh_lego_arch.png?raw=true "Solution architecture diagram")

### Todo


