# 🚀 Pokémon IAM Challenge API

![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
![JWT Auth](https://img.shields.io/badge/JWT_Auth-✓-green)
![Python](https://img.shields.io/badge/Python-3.9+-yellow?logo=python)

API para gestión de Pokémon con autenticación JWT e integración de datos climáticos.

## 📋 Tabla de Contenidos
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Autenticación](#-autenticación)
- [Endpoints](#-endpoints)
- [Ejemplos](#-ejemplos)
- [Despliegue](#-despliegue)
- [Seguridad](#-seguridad)

## 🔧 Requisitos
- **Python 3.9+**
- **Docker** (recomendado para entornos consistentes)
- **Docker Compose** (v2.0+)

## 🛠 Instalación

### Opción 1: Entorno Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor (modo desarrollo)
flask run --host=0.0.0.0 --port=5000

Opción 2: Docker (Recomendado)

# Construir y ejecutar
docker-compose up --build

# Solo ejecutar (si ya está construido)
docker-compose up

🔐 Autenticación JWT
La API usa JSON Web Tokens para autenticación. Debes incluir el token en el header Authorization.

Obtener Token

curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"$ADMIN_PASSWORD"}'

  Nota: Configura las credenciales en el archivo .env (ver Seguridad).

🌐 Endpoints
🐉 Pokémon
Método	Endpoint	Descripción	Requiere Auth
GET	/pokemon/<nombre>	Obtener tipo de Pokémon	✅
GET	/random-pokemon/<tipo>	Pokémon aleatorio por tipo	✅
GET	/longest-name/<tipo>	Pokémon con nombre más largo	✅
🌦️ Clima
| GET | /weather?city=<ciudad> | Obtener temperatura actual | ✅ |
| GET | /strongest-pokemon?city=<ciudad> | Pokémon más fuerte según clima | ✅ |

🔄 Tokens
| POST | /refresh | Refrescar access token | ✅ (refresh token) |
| DELETE | /logout | Invalidar token | ✅ |

📖 Ejemplos
Flujo Completo

# 1. Autenticación
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"$ADMIN_PASSWORD"}' | jq -r '.access_token')

# 2. Consultar Pokémon
curl -X GET http://localhost:5000/pokemon/pikachu \
  -H "Authorization: Bearer $TOKEN"

# 3. Consultar clima
curl -X GET "http://localhost:5000/weather?city=Bogota"

# 4. Cerrar sesión
curl -X DELETE http://localhost:5000/logout \
  -H "Authorization: Bearer $TOKEN"

  Salidas Esperadas
<details> <summary>Ver ejemplos JSON</summary>
Pokémon:

json
Copy
{"name": "pikachu", "type": "electric"}
Clima:

json
Copy
{"city": "Bogota", "temperature": 14.5, "unit": "C"}
Pokémon + Clima:

json
Copy
{
  "city": "Medellin",
  "temperature": 24.0,
  "strongest_type": "ground",
  "random_pokemon": "onix"
}
</details>
🐳 Despliegue con Docker
Comandos Esenciales
bash
Copy
# Construir imagen
docker build -t pokemon-iam .

# Ejecutar contenedor
docker run -p 5000:5000 --env-file .env pokemon-iam

# Ver logs
docker-compose logs -f
Estructura del Proyecto
Copy
pokemon-iam/
├── app.py              # Lógica principal
├── Dockerfile          # Configuración Docker
├── docker-compose.yml  # Orquestación
├── requirements.txt    # Dependencias
└── .env.example        # Plantilla de variables
🔒 Seguridad
Configuración Requerida
Crear archivo .env basado en .env.example:

ini
Copy
JWT_SECRET_KEY=tu_clave_super_secreta
ADMIN_PASSWORD=contraseña_fuerte
Buenas Prácticas:

Nunca comitear archivos .env

Usar HTTPS en producción

Rotar tokens regularmente

Recomendaciones para Producción
Usar base de datos real (PostgreSQL/MySQL)

Implementar rate limiting

Configurar HTTPS con certificados válidos

Usar gestores de secrets (Hashicorp Vault/AWS Secrets Manager)

⁉️ Soporte
Para problemas o preguntas, abre un issue en el repositorio.

✨ Tip: Usa jq para procesar respuestas JSON en bash (sudo apt install jq en Ubuntu)

