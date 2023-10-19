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

create_data_dirs() {
    log "Creating data directories..."
    mkdir -p data/raw data/stg data/processed data/garbage
    log "Data directories created successfully."
}

move_to_garbage() {
    local dir_to_clean=$1
    log "Moving all files from $dir_to_clean to data/garbage..."
    mv $dir_to_clean/* data/garbage/ 2>/dev/null
    log "Moved all files from $dir_to_clean to data/garbage."
}

clean_data() {
    if [[ "$1" == "--clean" ]]; then
        move_to_garbage "data/raw"
        move_to_garbage "data/stg"
        move_to_garbage "data/processed"
    elif [[ "$1" == "--dir" && -n "$2" ]]; then
        move_to_garbage "data/$2"
    else
        log "Invalid option for data clean."
    fi
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
        manage)
            echo "Usage: ./setup.sh manage [SUBCOMMAND] [OPTION]"
            echo "  structure --create, -c  Create data directories."
            echo "  structure --clean       Move all files from raw, stg, processed to garbage."
            # echo "  clean --all             Move all files from raw, stg, processed to garbage."
            # echo "  clean --dir [DIR]       Move all files from specified dir to garbage."
            ;;
        *)
            echo "Usage: ./setup.sh [COMMAND] [OPTION]"
            echo "Available commands:"
            echo "  --help, -h       Display this help message."
            echo "  all              Execute the complete setup flow."
            echo "  env              Only create the .env files."
            echo "  airflow          Set up Airflow."
            echo "  manage           Data helping commands."
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
        # Aquí deberías tener tu función setup_airflow
        ;;
    manage)
        case "$2" in
            structure)
                if [[ "$3" == "--create" || "$3" == "-c" ]]; then
                    create_data_dirs
                elif [[ "$3" == "--clean" ]]; then
                    clean_data "$3" "$4"
                else
                    log "Invalid option for manage structure."
                fi
                ;;
            *)
                log "Invalid subcommand for manage."
                show_help manage
                ;;
        esac
        ;;
    *)
        echo "Unrecognized or not provided option."
        show_help
        ;;
esac
