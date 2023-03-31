# Data_Pipeline_Ethereum_Token   

This project is designed to extract ERC20 token data from Web3 using the Etherscan API and create an ETL pipeline using Apache Airflow. The extracted data is scheduled to be fed into a local PostgreSQL database daily. The project involves technologies such as Docker, Airflow DAGs, PostgreSQL, and HDFS. Below is the screenshot of the data pipeline in action.  
![image](https://user-images.githubusercontent.com/117455557/229133404-fe19a6b3-2545-4a31-b340-9726900ca8a7.png)  

## Extraction  
We extract data from the Ethereum blockchain using the Etherscan API, which provides access to a vast array of blockchain data, including ERC20 token transfers. The API is queried daily to retrieve the latest ERC20 token data.  

## Transformation  
Once the data is extracted, it is transformed using a series of tasks to clean, adjust and transpose the data. This ensures that the data is accurate, clean and readable for analysis. The transform tasks are implemented using Python scripts and executed using Apache Airflow.  

## Loading  
The transformed data is then loaded into a PostgreSQL database for analysis. The data is sorted in descending order by datetime to facilitate analysis and visualization. The PostgreSQL database can be accessed using tools such as Beaver or other SQL clients.  
![image](https://user-images.githubusercontent.com/117455557/229133515-f30d54b4-e8cf-42ee-9e6f-19e9d3e1a572.png)  

## Requirements  
- Docker installed on your machine  
- An Airflow installation (you can use the official Apache Airflow Docker image)  
- A PostgreSQL database (or another database supported by Airflow)  

## Setting up the Environment  
1. Open the docker-compose.yaml file and go to the "services" section to find the PostgreSQL section.  

2. Under the volumes section, enter ports: -5432:5432. The modified section should look like this  
![image](https://user-images.githubusercontent.com/117455557/229131423-87556da8-eacd-4994-83ec-144a5c10018e.png)  

3. Run the command docker-compose up airflow-init in the terminal.  

4. Run the command docker-compose up in the same terminal. This command keeps the terminal running and refreshing your system. Alternatively, if the PostgreSQL image is already set up and you only need to change the PostgreSQL section, you can run docker-compose up -d --nodeps --build postgres.  

5. Go to the "Beaver" Windows app and add a PostgreSQL server.  

6. Set the username and password for the PostgreSQL server as "airflow".  

7. Add a database in PostgreSQL by clicking the right button in the database section. In this case, we named the database "erc20_database".  

8. Go to the Airflow UI, select "Admin" -> "Connections" -> "+ (Add Connection)".  

9. In the "Add Connection" form, fill in the following details:  
- Connection Id: eth_localhost (make sure the DAG postgres_conn_id matches this connection ID).
- Connection Type: Postgres
- Host: host.docker.internal
- Schema: erc20_database (make sure the schema name matches the database name you added in step 7).
- Login and Password: both set to "airflow"
- Port: 5432  

10. After setting up everything, click the "Test Connection" button to check if it is successful.  

## Usage  
Once the containers are running, you can use the Airflow UI to manage and monitor the pipeline. The pipeline consists of several DAGs, each of which represents a different step in the process. You can use the UI to trigger DAG runs, monitor task progress, and view logs.  
