# TDH Lego Truck Big Data Challenge
TDH Lego Truck Big Data Challenge No.3 solution. 

## Description
The solution outline below uses Python tools and libraries to process the data. These are organised using docker images/containers to ease reproducing the results. 

The batch processing uses Pandas to load, enrich and aggregate the data. It is presented in a Jupyter notebook.

The streaming solution was implemented using Kafka for stream processing and MongoDB as the database. 

Please see below for specific instructions on each of the challenge's sections, together with  comments on the assumptions made and known issues. 

## Batch Processing
A container was created to run the batch processing. Run it using the commands below: 

 1. Create the network shared by all containers:

   ```docker network create kafka-network```

2. Run the container with the Jupyter notebook server:

   ```docker-compose -f docker-compose.jupyter.yml up --build```

The last command will launch a Jupyter notebook. Navigate and run the notebook `batch.ipynb`.

This notebook contains all the code to load the data and process it according to the challenge instructions. 

### Assumptions

**Mean acceleration:** calculated using the scalar mean; this does not take into account the direction of the acceleration. Acceleration was computed as the square root of the sum of each of it's axial components sum (sqrt(x^2+y^2+z^2)). 
This was stored in a Pandas dataframe column. 

**Jerk:** based on the previous assumption computed jerk as the delta acceleration over delta time. This were computed for each individual dataset. Three new columns were added (`delta_accel`, `delta_time` and `jerk`).

## Stream Processing 

_Note: This solution was adopted from the code/tutorial found on: 
[Building A Streaming Fraud Detection System With Kafka And Python](https://blog.florimondmanca.com/building-a-streaming-fraud-detection-system-with-kafka-and-python)._ 

The solution uses Kafka to interact with the data streaming and consuming scripts. Kafka is used via the `kafka-python` Python library, which interfaces the underlying Kafka. The following image describes the architecture: 

![Alt text](/img/tdh_lego_arch.png?raw=true "Streaming solution architecture diagram")

The project is organised in docker containers as follows: 
* `docker-compose.yml`: starts two  services: a generator and a detector. Both services interact ith the Kafka broker and are started at the same time. The generator service loads the csv files and publishes them to the Kafka broker, simulating a streaming application. The detector service consumes the same topic from  the Kafka broker. The detector app also enriches each data row, adding two fields: `break_event` and `rgt_turn`. The final data row is then inserted into the MondoDB collection;
* `docker-compose.kafka.yml`: container for the Kafka and Zookeeper services. This should be the first container to run;
* `docker-compose.mongo.yml`: MongoDB server container. 

### Running the containers/scripts
The following commands will launch the containers needed to run the solution, as well as start the scripts that stream and store the data: 
1. Create the network shared by all containers (please skip this step if you have already created this network for the batch processing notebook described above):

   ```docker network create kafka-network```
1. Start the Kafka broker:

    ```docker-compose -f docker-compose.kafka.yml up --build``` 
2. Start the MongoDB container:

   ```docker-compose -f docker-compose.mongo.yml up --build```
3. Start the generator/detector:
  
   ```docker-compose up --build```

The last command will start the generator and detector scripts. The generator will load all files and send messages to the kafka broker, publishing on the `queueing.transactions` topic. The detector consumes this topic and enriches each message/row with domain specific information (break and right turn information). Each processed message is then inserted in the MongoDB database.

To query the MongoDB collection you can use the following Jupyter notebook (run from the docker container): 
   
   ```notebooks/db_query.ipynb```

This notebook executes a very simple query on the `lego.test` collection,  printing all entries that have been populated by the detector script.

### Assumptions
Two fields were added to each row: 
* `break_event`: True if `accel_x` is positive, False if negative and None otherwise;
* `rgt_turn`: True if `gyro_yaw` is positive, False if negative and None otherwise.

## Known issues
* The detector script is inserting the rows immediately, when it should be inserting the results every _n_ seconds; 
* The data folder is not shared by both solutions (duplicate data);
* The Mongodb database is not being saved in a local folder (not persisting);
* no tests were written.
