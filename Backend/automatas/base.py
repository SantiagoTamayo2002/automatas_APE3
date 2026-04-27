from abc import ABC, abstractmethod
from typing import Set, List, Dict, Any


class AFNDSimulator(ABC):
    """
    Clase base abstracta para simuladores de AFND.
    Maneja múltiples estados simultáneos según la definición formal:
    δ: Q × Σ → P(Q)
    """

    def __init__(self):
        self.states: Set[str] = set()
        self.alphabet: List[str] = []
        self.transitions: Dict[str, Dict[str, Set[str]]] = {}
        self.initial_state: str = ""
        self.accept_states: Set[str] = set()
        self._setup()

    @abstractmethod
    def _setup(self):
        """Inicializa los componentes del autómata (Q, Σ, δ, q0, F)."""
        pass

    def get_next_states(self, current_state: str, token: str) -> Set[str]:
        """Retorna el conjunto de estados siguientes dado un estado y token."""
        return self.transitions.get(current_state, {}).get(token, set())

    def simulate(self, input_tokens: List[str]) -> Dict[str, Any]:
        """
        Simula el AFND con la cadena de entrada.
        
        Args:
            input_tokens: Lista de tokens a procesar.
            
        Returns:
            Diccionario con traza de ejecución y resultado final.
        """
        current_states: Set[str] = {self.initial_state}
        trace = []

        # Paso inicial
        trace.append({
            "step": 0,
            "token": None,
            "states_before": list(current_states),
            "states_after": list(current_states),
            "description": f"Estado inicial: {{{', '.join(sorted(current_states))}}}"
        })

        for idx, token in enumerate(input_tokens):
            # Validar token en alfabeto
            if token not in self.alphabet:
                return {
                    "accepted": False,
                    "trace": trace,
                    "final_states": [],
                    "error": f"Token '{token}' no pertenece al alfabeto {self.alphabet}"
                }

            states_before = set(current_states)
            next_states: Set[str] = set()

            for state in current_states:
                next_states |= self.get_next_states(state, token)

            trace.append({
                "step": idx + 1,
                "token": token,
                "states_before": sorted(list(states_before)),
                "states_after": sorted(list(next_states)),
                "description": (
                    f"δ({{{', '.join(sorted(states_before))}}}, {token}) = "
                    f"{{{', '.join(sorted(next_states)) if next_states else '∅'}}}"
                )
            })

            current_states = next_states

            if not current_states:
                return {
                    "accepted": False,
                    "trace": trace,
                    "final_states": [],
                    "result_message": "Cadena RECHAZADA: no hay estados activos."
                }

        accepted = bool(current_states & self.accept_states)
        return {
            "accepted": accepted,
            "trace": trace,
            "final_states": sorted(list(current_states)),
            "result_message": (
                "Cadena ACEPTADA ✓" if accepted
                else "Cadena RECHAZADA: estados finales no son de aceptación."
            )
        }


    def get_definition(self) -> Dict[str, Any]:
        """Retorna la definición formal del autómata para el frontend."""
        serializable_transitions = {}
        for state, trans in self.transitions.items():
            serializable_transitions[state] = {
                token: sorted(list(targets))
                for token, targets in trans.items()
            }
        return {
            "states": sorted(list(self.states)),
            "alphabet": self.alphabet,
            "transitions": serializable_transitions,
            "initial_state": self.initial_state,
            "accept_states": sorted(list(self.accept_states)),
        }
