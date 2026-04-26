from .base import AFNDSimulator


class IoTProtocolAFND(AFNDSimulator):
    """
    Valida paquetes IoT con estructura: HDR (TEMP | HUM)* CRC
    
    Estados:
        q0 - Inicio (esperando HDR)
        q1 - HDR leído (esperando sensores o CRC)
        q2 - Sensor leído (esperando más sensores o CRC)
        q3 - CRC leído (aceptación)
    """

    def _setup(self):
        self.states = {"q0", "q1", "q2", "q3"}
        self.alphabet = ["HDR", "TEMP", "HUM", "CRC"]
        self.initial_state = "q0"
        self.accept_states = {"q3"}
        self.transitions = {
            "q0": {"HDR": {"q1"}},
            "q1": {"TEMP": {"q2"}, "HUM": {"q2"}, "CRC": {"q3"}},
            "q2": {"TEMP": {"q2"}, "HUM": {"q2"}, "CRC": {"q3"}},
            "q3": {}
        }

    def get_definition(self):
        base = super().get_definition()
        base.update({
            "name": "Protocolo de Telemetría IoT",
            "description": "Valida paquetes IoT: HDR (TEMP | HUM)* CRC",
            "language": "L = { HDR (TEMP | HUM)* CRC }",
            "state_labels": {
                "q0": "Inicio",
                "q1": "HDR ok",
                "q2": "Sensor",
                "q3": "Válido ✓"
            },
            "examples": {
                "valid": [
                    ["HDR", "CRC"],
                    ["HDR", "TEMP", "CRC"],
                    ["HDR", "HUM", "TEMP", "CRC"],
                    ["HDR", "TEMP", "HUM", "TEMP", "CRC"]
                ],
                "invalid": [
                    ["HDR"],
                    ["CRC"],
                    ["HDR", "HDR", "CRC"],
                    ["TEMP", "CRC"]
                ]
            }
        })
        return base
