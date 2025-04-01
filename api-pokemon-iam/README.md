# API Pokémon IAM Challenge 🚀

## 🔧 Requisitos
- Python 3.9+
- Docker (opcional)

## 🛠 Instalación
```bash
# Opción 1: Sin Docker
pip install -r requirements.txt
flask run

# Opción 2: Con Docker
docker-compose up --build
```

## 🔐 Autenticación
1. Obtén tu token JWT:
```bash
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{"username":"admin", "password":"P0k3M3l1..*"}'
```

## 🌐 Endpoints Clave
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/pokemon/<nombre>` | Tipo de Pokémon |
| `GET` | `/strongest-pokemon?city=<ciudad>` | Pokémon por clima local |

## 🐳 Dockerización
```bash
# Construir imagen
docker build -t pokemon-iam .

# Ejecutar contenedor
docker run -p 5000:5000 pokemon-iam
```

## 📌 Notas Importantes
- Claves JWT (Jason web token) es usado para devolver un token web y  se gestionan via `.env`
- Usuarios son de demostración (en producción usar DB y un gestor como AWS Secret Manager, o thicotyc, entre los mas seguros)