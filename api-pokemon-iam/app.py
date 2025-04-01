from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
import os
from dotenv import load_dotenv
import requests
import random
import logging
import subprocess

blacklist = set()

# Configuración básica
load_dotenv()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Necesario para JWT
jwt = JWTManager(app)

def load_users():
    """Carga usuarios desde .env"""
    users = {}
    for key, value in os.environ.items():
        if key.startswith("USER_"):
            username = key[5:].lower()
            password, role = value.split('|')
            users[username] = {"password": password, "role": role}
    return users

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

coordinates = {
    # Colombia
    "Bogota": {"latitude": 4.7110, "longitude": -74.0721},
    "Medellin": {"latitude": 6.2442, "longitude": -75.5812},
    "Cali": {"latitude": 3.4516, "longitude": -76.5320},
    # Argentina
    "Buenos Aires": {"latitude": -34.6118, "longitude": -58.4173}
}

# Helper functions
def fetch_pokemon_type(name):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}", timeout=5)
        if response.status_code == 200:
            return response.json()["types"][0]["type"]["name"]
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Pokémon type: {str(e)}")
        return None

def fetch_pokemon_by_type(pokemon_type):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/type/{pokemon_type.lower()}", timeout=5)
        if response.status_code == 200:
            # Extraer nombres base únicos (sin formas alternativas)
            pokemon_list = []
            for pokemon in response.json()["pokemon"]:
                base_name = pokemon["pokemon"]["name"].split("-")[0]
                if base_name not in pokemon_list:
                    pokemon_list.append(base_name)
            return pokemon_list
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Pokémon by type: {str(e)}")
        return None

def fetch_weather(latitude, longitude):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()["current_weather"]["temperature"]
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather: {str(e)}")
        return None

def get_strongest_type(temperature):
    if temperature >= 30:
        return "fire"
    elif temperature >= 20:
        return "ground"
    elif temperature >= 10:
        return "normal"
    elif temperature >= 0:
        return "water"
    else:
        return "ice"

# Endpoints
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", "").lower()
    password = request.json.get("password", "")
    
    users = load_users()

    if username in users and password == users[username]["password"]:
        access_token = create_access_token(
            identity=username,
            additional_claims={"role": users[username]["role"]}
        )
        refresh_token = create_refresh_token(identity=username)
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": users[username]["role"]
        })
    
    return jsonify({"error": "Invalid credentials"}), 401
    # Generar tokens
    access_token = create_access_token(
        identity=username,
        additional_claims={"role": role}
    )
    refresh_token = create_refresh_token(identity=username)
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }) 
 
# endpoint para refrescar el token de acceso
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": new_access_token})

# endpoint para revocar el token de acceso
@app.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

# endpoint para buscar pokemon por nombre
@app.route("/pokemon/<name>", methods=["GET"])
@jwt_required()
def get_pokemon_type(name):
    pokemon_type = fetch_pokemon_type(name)
    if not pokemon_type:
        return jsonify({"error": "Pokémon not found"}), 404
    return jsonify({"name": name, "type": pokemon_type})

#endoint para buscar pokemon por tipo
@app.route("/random-pokemon/<type>", methods=["GET"])
@jwt_required()
def get_random_pokemon(type):
    pokemon_list = fetch_pokemon_by_type(type)
    if not pokemon_list:
        return jsonify({"error": "No Pokémon found for this type"}), 404
    return jsonify({"type": type, "random_pokemon": random.choice(pokemon_list)})

#endpoint para buscar el pokemon con el nombre más largo por tipo
@app.route("/longest-name/<type>", methods=["GET"])
@jwt_required()
def get_longest_name_pokemon(type):
    pokemon_list = fetch_pokemon_by_type(type)
    if not pokemon_list:
        return jsonify({"error": "No Pokémon found for this type"}), 404
    return jsonify({
        "type": type,
        "longest_name": max(pokemon_list, key=lambda x: len(x))
    })

#endpoint para obtener el clima
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", default="Bogota")
    
    if city not in coordinates:
        return jsonify({
            "error": "City not supported",
            "available_cities": list(coordinates.keys())
        }), 400

    temp = fetch_weather(
        coordinates[city]["latitude"],
        coordinates[city]["longitude"]
    )
    
    if temp is None:
        return jsonify({"error": "Failed to fetch weather data"}), 500
        
    return jsonify({
        "city": city,
        "temperature": temp,
        "unit": "C"
    })

#endpoint para obtener el pokemon más fuerte
@app.route("/strongest-pokemon", methods=["GET"])
@jwt_required()
def get_strongest_pokemon():
    city = request.args.get("city", default="Bogota")
    
    if city not in coordinates:
        return jsonify({
            "error": "City not supported",
            "available_cities": list(coordinates.keys())
        }), 400

    temp = fetch_weather(
        coordinates[city]["latitude"],
        coordinates[city]["longitude"]
    )
    
    if temp is None:
        return jsonify({"error": "Failed to fetch weather data"}), 500

    strongest_type = get_strongest_type(temp)
    pokemon_list = fetch_pokemon_by_type(strongest_type)
    
    if not pokemon_list:
        return jsonify({"error": "No Pokémon found for this type"}), 404
    
    filtered = [
        p for p in pokemon_list
        if any(letter in p.lower() for letter in ["i", "a", "m"])
    ]
    
    if not filtered:
        return jsonify({
            "error": "No matching Pokémon found",
            "details": f"No Pokémon of type {strongest_type} contain 'I', 'A', or 'M'"
        }), 404
    
    return jsonify({
        "city": city,
        "temperature": temp,
        "strongest_type": strongest_type,
        "random_pokemon": random.choice(filtered),
        "description": f"Random {strongest_type}-type Pokémon containing 'I', 'A', or 'M'"
    })

if __name__ == "__main__":
    app.run(debug=True)