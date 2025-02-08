# airflow-2.10.4

# Steps to execute

1. Assumptions and Software needed
    - Docker 
    - Docker compose
    - Needs to have the capacity run 8 containers locally
2. Execute the following
    - ` docker compose airflow-init`
    - This is going to setup the initial docker environment and `user_id` and `password` (defaulted to airflow)
    - Set up the following folders locally. As these exists when you download this repo. It will might error out. You ignore them
        - `./dags` - All the generic dag code is present in this folder
        - `./logs` - contains logs from task execution and scheduler.
        - `./config` - Has airflow.cfg file to play with the parameters that we are interested in.
        - `./plugins` - I didn't add anything here. So didn't push it to git. airflow-init will create it for you.
        - `./datastore-data` - This is created as part of datastore emulator set up but for some reason, its not mounting back to local. So I didn't push it, it shouldn't effect the run.
3. Once successful
    - `docker compose up`
    - It should spin up the following containers
        - *postgres:13*
        - *redis:7.2-bookworm*
        - *airflow-webserver* : The webserver is available at `http://localhost:8080`
        - *airflow-scheduler* :  The scheduler monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
        - *airflow-worker* : The worker node to execute the tasks given by the scheduler.
        - *airflow-triggerer* : The triggerer runs an event loop for deferrable tasks.
        - *flower* : The flower app for monitoring the environment. It is available at `http://localhost:5555`
        - *datastore*
4. Navigate to `./airflow-2.10.4/datastore-code/`
    - execute `python3 datastore_write.py` (*feel free to add more entities*)
5. Acccess the airflow UI - `http://localhost:8080` and trigger the dags. (*They are defaulted to pause on spinup*)

# Important files to look at

1. `main.py` : Entry point for the airflow to trigger the dag generation
2. `dag_generator.py` : Parses the entry in the datastore-emulator and creates the tasks and dags
3. `operatory_factory.py` : Static objects to create the operators within tasks on demand
