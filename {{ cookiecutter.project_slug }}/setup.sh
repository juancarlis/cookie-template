#!/bin/bash

# Log directory
LOG_DIR="logs/setup"
mkdir -p $LOG_DIR
LOG_FILE="$LOG_DIR/setup.log"

# Function to log messages to the log file and display them on the console
log() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" | tee -a $LOG_FILE
}

create_env_files() {
    log "Creating .env files..."
    echo 'ENVIRONMENT="DEV"' > .env
    cat <<EOL > .env.dev
# DEV ENVIRONMENT
# DB example structure
# db_name_TYPE='mysql'
# db_name_USERNAME='user'
# db_name_PASSWORD='password'
# db_name_DATABASE='somedb'
# db_name_HOST='somehost.com'
EOL
    cat <<EOL > .env.prd
# PRD ENVIRONMENT
# DB example structure
# db_name_TYPE='mysql'
# db_name_USERNAME='user'
# db_name_PASSWORD='password'
# db_name_DATABASE='somedb'
# db_name_HOST='somehost.com'
EOL
    log ".env files created successfully."
}

setup_airflow() {
    local version="stable"
    if [[ "$1" == "--version" && -n "$2" ]]; then
        version="$2"
    fi

    log "Setting up Airflow..."
    if [[ ! -d "./airflow" ]]; then
        mkdir ./airflow
    fi

    if ! curl -LfO "https://airflow.apache.org/docs/apache-airflow/$version/docker-compose.yaml"; then
        log "Error: Failed to download Airflow version $version. Please check the available versions at: https://airflow.apache.org/docs/apache-airflow/"
        exit 1
    fi

    mv docker-compose.yaml ./airflow/
    mkdir -p ./airflow/dags ./airflow/logs ./airflow/plugins ./airflow/config
    echo -e "AIRFLOW_UID=$(id -u)" >> ./.env
    log "Airflow setup completed with version $version."
}

show_help() {
    case "$1" in
        airflow)
            echo "Usage: ./setup.sh airflow [OPTION]"
            echo "Available options for airflow:"
            echo "  --help, -h       Display this help message."
            echo "  --stable         Download the stable version of docker-compose.yaml (default)."
            echo "  --version v.x.z  Download the specified version of docker-compose.yaml."
            ;;
        all)
            echo "Usage: ./setup.sh all [OPTION]"
            echo "Available options for all:"
            echo "  --help, -h       Display this help message."
            echo "  --no-airflow     Execute the complete setup flow without setting up Airflow."
            ;;
        *)
            echo "Usage: ./setup.sh [OPTION]"
            echo "Available options:"
            echo "  --help, -h       Display this help message."
            echo "  all              Execute the complete setup flow."
            echo "  env              Only create the .env files."
            echo "  airflow          Set up Airflow."
            ;;
    esac
}

# Option handling
case "$1" in
    --help|-h)
        show_help
        ;;
    all)
        if [[ "$2" == "--help" || "$2" == "-h" ]]; then
            show_help all
            exit 0
        fi
        create_env_files
        if [[ "$2" != "--no-airflow" ]]; then
            setup_airflow
        fi
        log "Executing poetry install..."
        poetry install 2>&1 | tee -a $LOG_FILE
        log "Poetry install completed."
        log "Complete setup finished."
        ;;
    env)
        if [[ "$2" == "--help" || "$2" == "-h" ]]; then
            show_help env
            exit 0
        fi
        create_env_files
        ;;
    airflow)
        if [[ "$2" == "--help" || "$2" == "-h" ]]; then
            show_help airflow
            exit 0
        fi
        setup_airflow "$2" "$3"
        ;;
    *)
        echo "Unrecognized or not provided option."
        show_help
        ;;
esac
