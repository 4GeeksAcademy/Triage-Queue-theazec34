# Triage-Queue-theazec34

Sistema de cola de triaje para urgencias hospitalarias, implementado en Python (solo biblioteca estándar). Gestiona pacientes por nivel de prioridad y orden de llegada.

## Estructura del proyecto

```
.
├── triage_queue.py   # Clases Patient, TriageQueue y menú CLI
├── DESIGN.md         # Notas de diseño (estructura de datos y concurrencia)
└── README.md
```

## Requisitos

- Python 3.10 o superior
- Solo biblioteca estándar (`collections.deque`, `dataclasses`, `datetime`)

## Ejecución

```bash
python triage_queue.py
```

Se abrirá un menú interactivo en español con estas opciones:

1. **Encolar paciente** — nombre y nivel de triaje (1=Crítico, 2=Urgente, 3=Estándar)
2. **Desencolar** — llama al siguiente paciente y lo elimina de la cola
3. **Peek** — muestra el siguiente paciente sin eliminarlo
4. **Listar cola** — todos los pacientes en orden de atención
5. **Estadísticas** — conteo por nivel de triaje
6. **Salir**

## Lógica de prioridad

- **Entre niveles:** nivel 1 siempre antes que 2, y 2 antes que 3.
- **Dentro del mismo nivel:** orden de llegada (FIFO).
- **Eficiencia:** `enqueue` y `dequeue` en O(1) gracias a tres colas `deque` (una por nivel).

## Componentes principales

### `Patient`

- `name`: nombre del paciente
- `triage_level`: entero 1, 2 o 3
- `arrived_at`: marca de tiempo de llegada

### `TriageQueue`

| Método | Descripción |
|---|---|
| `enqueue(patient)` | Añade un paciente respetando prioridad y FIFO |
| `dequeue()` | Elimina y devuelve el siguiente paciente; error descriptivo si la cola está vacía |
| `peek()` | Devuelve el siguiente paciente sin eliminarlo |
| `list_queue()` | Lista en orden de atención |
| `stats()` | Diccionario `{1: n1, 2: n2, 3: n3}` con pacientes en espera |

## Casos borde

- Cola vacía: `dequeue()` y `peek()` lanzan `EmptyQueueError` con mensaje claro; el CLI no se cae.
- Nivel de triaje inválido: se rechaza al crear el `Patient`.
- Entradas vacías en el CLI: se vuelve a pedir al usuario.

## Diseño

Ver [DESIGN.md](./DESIGN.md) para la justificación de tres `deque` frente a otras estructuras y el enfoque de concurrencia con candados.
