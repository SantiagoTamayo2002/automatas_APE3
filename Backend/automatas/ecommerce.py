from .base import AFNDSimulator


class EcommerceAFND(AFNDSimulator):
    """
    Detecta el patrón 'Comprador Potencial': HOME SEARCH+ CART
    
    Estados:
        q0 - Inicio
        q1 - HOME visitado
        q2 - SEARCH realizado (uno o más)
        q3 - CART visitado (aceptación)
    """

    def _setup(self):
        self.states = {"q0", "q1", "q2", "q3"}
        self.alphabet = ["HOME", "SEARCH", "CART"]
        self.initial_state = "q0"
        self.accept_states = {"q3"}
        self.transitions = {
            "q0": {"HOME": {"q1"}},
            "q1": {"SEARCH": {"q2"}},
            "q2": {"SEARCH": {"q2"}, "CART": {"q3"}},
            "q3": {}
        }

    def get_definition(self):
        base = super().get_definition()
        base.update({
            "name": "Comportamiento E-commerce",
            "description": "Detecta compradores potenciales: HOME SEARCH+ CART",
            "language": "L = { HOME SEARCH+ CART }",
            "state_labels": {
                "q0": "Inicio",
                "q1": "Home ok",
                "q2": "Buscando",
                "q3": "Potencial ✓"
            },
            "examples": {
                "valid": [
                    ["HOME", "SEARCH", "CART"],
                    ["HOME", "SEARCH", "SEARCH", "CART"],
                    ["HOME", "SEARCH", "SEARCH", "SEARCH", "CART"]
                ],
                "invalid": [
                    ["HOME", "CART"],
                    ["SEARCH", "CART"],
                    ["HOME", "SEARCH"],
                    ["CART"]
                ]
            }
        })
        return base
