from .base import AFNDSimulator

class ValidadorCerraduraAFND(AFNDSimulator):
    """
    Simula un validador de cerradura (intentos de acceso).
    """

    def _setup(self):
        self.states = {"q0", "q1", "q2", "q3", "q4", "block"}
        self.alphabet = ["OK", "BAD"]
        self.initial_state = "q0"
        self.accept_states = {"q4"}
        self.transitions = {
            "q0": {"OK": {"q4"}, "BAD": {"q1"}},
            "q1": {"OK": {"q4"}, "BAD": {"q2"}},
            "q2": {"OK": {"q4"}, "BAD": {"q3"}},
            "q3": {"OK": {"block"}, "BAD": {"block"}},
            "q4": {},
            "block": {}
        }

    def get_definition(self):
        base = super().get_definition()
        base.update({
            "name": "Validador de Cerradura",
            "description": "Validador de intentos de contraseña.",
            "language": "L = Acceso concedido antes de bloquear",
            "state_labels": {
                "q0": "0 Fallos",
                "q1": "1 Fallo",
                "q2": "2 Fallos",
                "q3": "3 Fallos",
                "q4": "Desbloqueado",
                "block": "Bloqueado"
            },
            "examples": {
                "valid": [
                    ["OK"],
                    ["BAD", "OK"],
                    ["BAD", "BAD", "OK"]
                ],
                "invalid": [
                    ["BAD", "BAD", "BAD"],
                    ["BAD", "BAD", "BAD", "OK"]
                ]
            }
        })
        return base
