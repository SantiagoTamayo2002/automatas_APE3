from .base import AFNDSimulator
from typing import List, Dict, Any, Set


class GeneticSequenceAFND(AFNDSimulator):
    """
    Detecta el patrón K G X* F dentro de una cadena de aminoácidos.
    
    Estados:
        q0 - Búsqueda (leyendo cualquier aminoácido)
        q1 - K leída
        q2 - KG leído
        q3 - KGX* leído
        q4 - Patrón completo encontrado (aceptación)
    """

    def _setup(self):
        self.states = {"q0", "q1", "q2", "q3", "q4"}
        self.alphabet = ["K", "G", "X", "F"]
        self.initial_state = "q0"
        self.accept_states = {"q4"}
        self.transitions = {
            "q0": {"K": {"q0", "q1"}, "G": {"q0"}, "X": {"q0"}, "F": {"q0"}},
            "q1": {"G": {"q2"}},
            "q2": {"X": {"q3"}, "F": {"q4"}},
            "q3": {"X": {"q3"}, "F": {"q4"}},
            "q4": {}
        }

    def get_definition(self):
        base = super().get_definition()
        base.update({
            "name": "Secuencias Genéticas",
            "description": "Detecta el patrón K G X* F en cadenas de aminoácidos",
            "language": "L = { w ∈ Σ* | w contiene K G X* F }",
            "state_labels": {
                "q0": "Búsqueda",
                "q1": "K leída",
                "q2": "KG leído",
                "q3": "KGX* leído",
                "q4": "Hallado ✓"
            },
            "examples": {
                "valid": [
                    ["K", "G", "F"],
                    ["K", "G", "X", "F"],
                    ["K", "G", "X", "X", "F"],
                    ["G", "K", "G", "X", "F"]
                ],
                "invalid": [
                    ["K", "F"],
                    ["G", "F"],
                    ["K", "G"],
                    ["K", "X", "F"]
                ]
            }
        })
        return base
