#!/bin/bash

# Cargar variables del .env (ruta absoluta para evitar errores)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/.env"

# Debug: Verificar que la variable se cargó (opcional)
echo "Contraseña cargada: $ADMIN_PASSWORD"

# Hacer la petición
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "'"$ADMIN_PASSWORD"'"
  }'