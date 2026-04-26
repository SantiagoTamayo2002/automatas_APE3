# Simulador AFND — FEIRNNR Computación
**Autómatas Finitos No Deterministas | APE 3**

Autores: Manuel Santiago Tamayo Moreno, Luis David Armijos Roblez  
Docente: José O. Guamán Q.  
Asignatura: Teoría de Autómatas y Computabilidad Avanzada

---

## Estructura del Proyecto

```
AFND_Luis/
├── Backend/
│   ├── app.py                   # Entrada Flask
│   ├── requirements.txt
│   ├── run.sh
│   ├── automatas/
│   │   ├── __init__.py          # Registro de autómatas
│   │   ├── base.py              # Clase base AFNDSimulator
│   │   ├── iot_protocol.py      # AFND #1: IoT
│   │   ├── genetic_sequence.py  # AFND #2: Genética
│   │   └── ecommerce.py         # AFND #3: E-commerce
│   └── routes/
│       └── api_routes.py        # Endpoints REST
└── Frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    ├── run.sh
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── data/api.js
        ├── styles/global.css
        └── components/
            ├── StateDiagram.jsx   # Diagrama SVG animado
            ├── TransitionTable.jsx
            ├── TokenInput.jsx
            └── SimulationTrace.jsx
```

---

## Autómatas Implementados

| ID | Nombre | Lenguaje |
|----|--------|----------|
| `iot` | Protocolo Telemetría IoT | `HDR (TEMP \| HUM)* CRC` |
| `genetica` | Secuencias Genéticas | `K G X* F` (dentro de cadena) |
| `ecommerce` | Comportamiento E-commerce | `HOME SEARCH+ CART` |

---

## Requisitos

- Python 3.8+
- Node.js 18+
- npm

---

## Instalación y Ejecución

### Terminal 1 — Backend

```bash
cd AFND_Luis/Backend
pip install -r requirements.txt
python app.py
```

El backend queda disponible en: `http://localhost:5000`

### Terminal 2 — Frontend

```bash
cd AFND_Luis/Frontend
npm install
npm run dev
```

La aplicación queda disponible en: `http://localhost:5173`

---

## API REST

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/automatas` | Lista todos los autómatas |
| `GET` | `/api/automatas/{key}` | Definición formal de un autómata |
| `POST` | `/api/simulate/{key}` | Simula una cadena |

### Ejemplo de simulación (curl)

```bash
curl -X POST http://localhost:5000/api/simulate/iot \
  -H "Content-Type: application/json" \
  -d '{"tokens": ["HDR", "TEMP", "CRC"]}'
```

### Respuesta

```json
{
  "success": true,
  "accepted": true,
  "result_message": "Cadena ACEPTADA ✓",
  "final_states": ["q3"],
  "trace": [
    {"step": 0, "token": null, "states_before": ["q0"], "states_after": ["q0"], ...},
    {"step": 1, "token": "HDR", "states_before": ["q0"], "states_after": ["q1"], ...},
    ...
  ]
}
```

---

## Agregar un nuevo autómata

1. Crear `Backend/automatas/mi_automata.py` heredando de `AFNDSimulator`
2. Implementar `_setup()` con `states`, `alphabet`, `transitions`, `initial_state`, `accept_states`
3. Importar y registrar en `Backend/automatas/__init__.py`
4. El frontend lo detecta automáticamente

---

## Repositorio

https://github.com/SantiagoTamayo2002/automatas_APE3
