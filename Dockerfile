FROM apache/airflow:2.6.3

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow
WORKDIR /opt/airflow

# Copy .env file (for local builds, but not in production)
COPY ./config/.env .  

# Copy requirements.txt first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

# Install additional Airflow providers
RUN pip install apache-airflow-providers-postgres requests python-dotenv pandas psycopg2-binary

# Copy DAGs, tasks, and configurations
COPY dags/ /opt/airflow/dags/
COPY config/ /opt/airflow/config/

# Add dags/ to PYTHONPATH so Airflow can find tasks
ENV PYTHONPATH="/opt/airflow/dags:$PYTHONPATH"

# Default command (overridden in docker-compose.yml)
CMD ["airflow", "webserver"]