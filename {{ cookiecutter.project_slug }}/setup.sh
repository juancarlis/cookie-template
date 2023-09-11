#!/bin/bash

# Directorio de logs
LOG_DIR="logs/setup"
mkdir -p $LOG_DIR
LOG_FILE="$LOG_DIR/setup.log"

# Función para registrar mensajes en el archivo de log y mostrarlos en la consola
log() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" | tee -a $LOG_FILE
}

# Verificar si solo se deben crear los archivos .env
if [ "$1" == "--env-only" ]; then
    log "Creando solo archivos .env..."
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
    log "Archivos .env creados exitosamente."
    exit 0
fi

# Flujo completo de configuración
log "Iniciando configuración completa..."

# Crear archivos .env
log "Creando archivos .env..."
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
log "Archivos .env creados exitosamente."

# Ejecutar poetry install
log "Ejecutando poetry install..."
poetry install 2>&1 | tee -a $LOG_FILE
log "Poetry install completado."

# (Otras acciones que quieras realizar)

log "Configuración completa finalizada."
