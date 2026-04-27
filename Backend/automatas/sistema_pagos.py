from .base import AFNDSimulator

class SistemaDePagosAFND(AFNDSimulator):
    """
    Simula un sistema de pagos.
    """

    def _setup(self):
        self.states = {"inicial", "autorizado", "cancelado", "capturado", "completado", "error"}
        self.alphabet = ["AUTH", "CANCEL", "CAP", "LIQ"]
        self.initial_state = "inicial"
        self.accept_states = {"completado"}
        self.transitions = {
            "inicial": {"AUTH": {"autorizado"}, "CANCEL": {"cancelado"}},
            "autorizado": {"CAP": {"capturado"}, "CANCEL": {"cancelado"}},
            "capturado": {"LIQ": {"completado"}},
            "completado": {"CANCEL": {"error"}},
            "cancelado": {},
            "error": {}
        }

    def get_definition(self):
        base = super().get_definition()
        base.update({
            "name": "Sistema de Pagos",
            "description": "Simula el flujo de estados de un sistema de pagos.",
            "language": "L = Flujos que terminan en completado",
            "state_labels": {
                "inicial": "Inicial",
                "autorizado": "Autorizado",
                "cancelado": "Cancelado",
                "capturado": "Capturado",
                "completado": "Completado",
                "error": "Error"
            },
            "examples": {
                "valid": [
                    ["AUTH", "CAP", "LIQ"]
                ],
                "invalid": [
                    ["AUTH", "CANCEL"],
                    ["AUTH", "CAP", "CANCEL"],
                    ["CANCEL"]
                ]
            }
        })
        return base
