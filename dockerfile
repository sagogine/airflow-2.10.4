# Use the base Airflow image
FROM apache/airflow:2.10.4

# Set the working directory
WORKDIR /opt/airflow

# Copy the requirements.txt to the container
COPY requirements.txt /opt/airflow/requirements.txt

# Install the additional dependencies
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Copy your DAGs and other files
COPY dags /opt/airflow/dags
COPY plugins /opt/airflow/plugins
COPY config /opt/airflow/config
