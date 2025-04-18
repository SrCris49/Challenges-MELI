# 🚀 Pokémon IAM Challenge API

![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
![JWT Auth](https://img.shields.io/badge/JWT_Auth-✓-green)
![Python](https://img.shields.io/badge/Python-3.9+-yellow?logo=python)

API para gestión de Pokémon con autenticación JWT e integración de datos climáticos.

## 📋 Tabla de Contenidos
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Autenticación](#-Autenticación_JWT)
- [Endpoints](#-endpoints)
- [Ejemplos](#-ejemplos)
- [Despliegue](#-Despliegue_con_Docker)
- [Seguridad](#-seguridad)

## 🔧 Requisitos
- **Python 3.9+**
- **Docker** (recomendado para entornos consistentes)
- **Docker Compose** (v2.0+)

## Descarga del repo
```bash
git clone git@github.com:SrCris49/api-pokemon-iam.git
cd api-pokemon-iam/api-pokemon-iam
```
## 🛠 Instalación

### Opción 1: Entorno Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor (modo desarrollo)
flask run --host=0.0.0.0 --port=5000
```

### Opción 2: Docker (Recomendado)
```bash
# Construir y ejecutar
docker-compose up --build

# Solo ejecutar (si ya está construido)
docker-compose up
```

## 🔐 Autenticación JWT
La API usa JSON Web Tokens para autenticación. Debes incluir el token en el header Authorization.

Obtener Token
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"<PASS DENTRO DE LA VARIABLE $USER_ADMIN DEL .ENV>"}'
```
  Nota: Configura las credenciales en el archivo .env (ver Seguridad).

🌦️ Clima
| GET | /weather?city=<ciudad> | Obtener temperatura actual | ❌ |

🔄 Tokens
| POST | /refresh | Refrescar access token | ✅ (refresh token) |
| DELETE | /logout | Invalidar token | ✅ |

## 📖 Ejemplos
Flujo Completo

# 1. Autenticación
```bash
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"$ADMIN_PASSWORD"}' | jq -r '.access_token')
```
# 2. Funcionamiento de los Endpoints

## 🌐 Endpoints
🐉 Pokémon

GET	/pokemon/<nombre>	Obtener tipo de Pokémon	✅
```bash
curl -X GET http://localhost:5000/pokemon/pikachu \
  -H "Authorization: Bearer $TOKEN"
```
GET	/random-pokemon/<tipo>	Pokémon aleatorio por tipo	✅
```bash
curl -X GET http://localhost:5000/random-pokemon/fire \
  -H "Authorization: Bearer $TOKEN"
```     
GET	/longest-name/<tipo>	Pokémon con nombre más largo	✅
```bash
curl -X GET http://localhost:5000/longest-name/water \
  -H "Authorization: Bearer $TOKEN"
```     
GET /strongest-pokemon?city=<ciudad> Pokémon más fuerte según clima  ✅
```bash
curl -X GET http://127.0.0.1:5000/strongest-pokemon?city=Cali \
  -H "Authorization: Bearer $TOKEN"
```  

# 3. Consultar clima
```bash
curl -X GET "http://localhost:5000/weather?city=Bogota"
```
# 4. Cerrar sesión
```bash
curl -X DELETE http://localhost:5000/logout \
  -H "Authorization: Bearer $TOKEN"
```
  Salidas Esperadas
  
Pokémon:
```bash
json
Copy
{"name": "pikachu", "type": "electric"}
  
```
Clima:
```bash
json
Copy
{"city": "Bogota", "temperature": 14.5, "unit": "C"}

```
Pokémon + Clima:
```bash
{
  "city": "Medellin",
  "temperature": 24.0,
  "strongest_type": "ground",
  "random_pokemon": "onix"
}
```

## 🐳 Despliegue con Docker
Comandos Esenciales
```bash
# Construir imagen
docker build -t pokemon-iam .

# Ejecutar contenedor
docker run -p 5000:5000 --env-file .env pokemon-iam

# Ver logs
docker-compose logs -f
````

Estructura del Proyecto

pokemon-iam/
├── app.py              # Lógica principal
├── Dockerfile          # Configuración Docker
├── docker-compose.yml  # Orquestación
├── requirements.txt    # Dependencias
└── .env.example        # Plantilla de variables

## 🔒 Seguridad
Configuración Requerida
Crear archivo .env basado en .env.example:

```bash
# Usuarios (formato: USER_<nombre>=<password>|<rol>)
USER_ADMIN=megaclave1234..|admin
USER_POKEMASTER=pokemon123|trainer
USER_GUEST=guest123|viewer
# Configuración JWT
JWT_SECRET_KEY=tu_clave_super_secreta_aqui
# APIS EXTERNAS
POKEAPI_URL=https://pokeapi.co/api/v2
WEATHER_API_URL=https://api.open-meteo.com/v1
```

Buenas Prácticas:

Nunca comitear archivos .env  #todo enviarlo al .gitignore

Usar HTTPS en producción

Rotar tokens regularmente

Recomendaciones para Producción:
Usar base de datos real (PostgreSQL/MySQL)

Configurar HTTPS con certificados válidos

Usar gestores de secrets (Hashicorp Vault/AWS Secrets Manager)
