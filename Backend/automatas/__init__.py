"""
Registro central de autómatas disponibles.
Para agregar un nuevo autómata, solo importarlo y añadirlo al diccionario.
"""
from .iot_protocol import IoTProtocolAFND
from .genetic_sequence import GeneticSequenceAFND
from .ecommerce import EcommerceAFND
from .sistema_pagos import SistemaDePagosAFND
from .orquestacion_pedidos import OrquestacionPedidosAFND
from .validador_cerradura import ValidadorCerraduraAFND

AUTOMATA_REGISTRY = {
    "iot": IoTProtocolAFND,
    "genetica": GeneticSequenceAFND,
    "ecommerce": EcommerceAFND,
    "pagos": SistemaDePagosAFND,
    "pedidos": OrquestacionPedidosAFND,
    "cerradura": ValidadorCerraduraAFND,
}

def get_automata(key: str):
    """Retorna una instancia del autómata solicitado."""
    cls = AUTOMATA_REGISTRY.get(key)
    if not cls:
        return None
    return cls()

def list_automata():
    """Lista todos los autómatas disponibles con su definición."""
    result = {}
    for key, cls in AUTOMATA_REGISTRY.items():
        instance = cls()
        result[key] = instance.get_definition()
    return result
