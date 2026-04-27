from .base import AFNDSimulator

class OrquestacionPedidosAFND(AFNDSimulator):
    """
    Simula la orquestación de pedidos.
    """

    def _setup(self):
        self.states = {"q_init", "q_cre", "q_emp", "q_can", "q_env", "q_ent", "q_dev"}
        self.alphabet = ["CREATE", "EMP", "CAN", "ENV", "ENT", "DEV"]
        self.initial_state = "q_init"
        self.accept_states = {"q_ent", "q_dev", "q_can"}
        self.transitions = {
            "q_init": {"CREATE": {"q_cre"}},
            "q_cre": {"EMP": {"q_emp"}, "CAN": {"q_can"}},
            "q_emp": {"ENV": {"q_env"}, "CAN": {"q_can"}},
            "q_env": {"ENT": {"q_ent"}},
            "q_ent": {"DEV": {"q_dev"}},
            "q_can": {},
            "q_dev": {}
        }

    def get_definition(self):
        base = super().get_definition()
        base.update({
            "name": "Orquestación de Pedidos",
            "description": "Simula la orquestación de estados de un pedido.",
            "language": "L = Pedidos entregados, devueltos o cancelados",
            "state_labels": {
                "q_init": "Inicio",
                "q_cre": "Creado",
                "q_emp": "Empaquetado",
                "q_can": "Cancelado",
                "q_env": "Enviado",
                "q_ent": "Entregado",
                "q_dev": "Devuelto"
            },
            "examples": {
                "valid": [
                    ["CREATE", "EMP", "ENV", "ENT"],
                    ["CREATE", "CAN"],
                    ["CREATE", "EMP", "ENV", "ENT", "DEV"]
                ],
                "invalid": [
                    ["CREATE", "ENV"],
                    ["EMP", "ENV"]
                ]
            }
        })
        return base
