from flask import Blueprint, request, jsonify
from automatas import get_automata, list_automata, AUTOMATA_REGISTRY

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/automatas", methods=["GET"])
def get_all_automata():
    """Retorna la lista de todos los autómatas disponibles con sus definiciones."""
    return jsonify({
        "success": True,
        "automatas": list_automata()
    })


@api_bp.route("/automatas/<string:automata_key>", methods=["GET"])
def get_automata_definition(automata_key: str):
    """Retorna la definición formal de un autómata específico."""
    automata = get_automata(automata_key)
    if not automata:
        return jsonify({
            "success": False,
            "error": f"Autómata '{automata_key}' no encontrado. Disponibles: {list(AUTOMATA_REGISTRY.keys())}"
        }), 404

    return jsonify({
        "success": True,
        "automata": automata.get_definition()
    })


@api_bp.route("/simulate/<string:automata_key>", methods=["POST"])
def simulate(automata_key: str):
    """
    Simula un AFND con la cadena proporcionada.
    
    Body JSON:
        { "tokens": ["TOKEN1", "TOKEN2", ...] }
    
    Response:
        {
            "accepted": bool,
            "trace": [...],
            "final_states": [...],
            "result_message": str
        }
    """
    automata = get_automata(automata_key)
    if not automata:
        return jsonify({
            "success": False,
            "error": f"Autómata '{automata_key}' no encontrado."
        }), 404

    data = request.get_json()
    if not data or "tokens" not in data:
        return jsonify({
            "success": False,
            "error": "El cuerpo debe contener el campo 'tokens' (lista de strings)."
        }), 400

    tokens = data["tokens"]
    if not isinstance(tokens, list):
        return jsonify({
            "success": False,
            "error": "'tokens' debe ser una lista."
        }), 400

    if len(tokens) == 0:
        return jsonify({
            "success": False,
            "error": "La cadena de entrada no puede estar vacía."
        }), 400

    if len(tokens) > 100:
        return jsonify({
            "success": False,
            "error": "La cadena no puede tener más de 100 tokens."
        }), 400

    # Normalizar a mayúsculas
    tokens = [str(t).strip().upper() for t in tokens]

    result = automata.simulate(tokens)
    return jsonify({
        "success": True,
        **result
    })
