# Notas de diseño — Cola de triaje

## Elección de estructura de datos

Se implementó `TriageQueue` con **tres colas `deque` independientes**, una por nivel de triaje (1, 2 y 3).

### ¿Por qué tres `deque` y no otras alternativas?

| Alternativa | Problema |
|---|---|
| **Un solo `deque`** | No respeta prioridad: un paciente nivel 3 encolado antes que uno nivel 1 sería atendido primero. Habría que reordenar o buscar en toda la cola. |
| **Lista ordenada** | Cada `enqueue` requiere insertar en la posición correcta (O(n)) y desplazar elementos. Con muchos pacientes, la inserción se vuelve costosa. |
| **`heapq` (montículo)** | Funciona para prioridad, pero empata por tupla `(nivel, timestamp)`. Requiere un contador monótono o comparación de `datetime` en cada operación, y el orden FIFO dentro del mismo nivel es menos directo que un `deque`. |

Con **tres `deque` separados**:

- `enqueue`: O(1) — se añade al final del `deque` del nivel correspondiente.
- `dequeue`: O(1) — se revisa nivel 1, luego 2, luego 3, y se hace `popleft()` en el primero no vacío.
- `peek`, `list_queue`, `stats`: O(n) en el peor caso al recorrer las colas, pero sin reordenar.

La regla de prioridad (1 > 2 > 3) y el FIFO dentro de cada nivel quedan garantizados de forma natural.

## Concurrencia

En un entorno con varios workers (por ejemplo, varias enfermeras usando el sistema a la vez), las operaciones sobre la cola deben ser **atómicas** para evitar condiciones de carrera:

1. **Candado compartido (`threading.Lock`)**: Todas las mutaciones (`enqueue`, `dequeue`) y lecturas consistentes (`peek`, `list_queue`, `stats`) se ejecutan dentro de `with self._lock:`.
2. **Orden de mutación en `dequeue`**: Primero identificar el nivel con pacientes, luego hacer `popleft()` bajo el candado. Así ningún otro worker puede desencolar al mismo paciente.
3. **Encolar crítico concurrente**: Si un worker encola un paciente nivel 1 mientras otro desencola, el candado serializa las operaciones. El paciente crítico quedará disponible en la siguiente `dequeue`, sin doble procesamiento ni pérdida de pacientes.

Ejemplo esquemático:

```python
import threading
from collections import deque

class TriageQueue:
    def __init__(self):
        self._queues = {1: deque(), 2: deque(), 3: deque()}
        self._lock = threading.Lock()

    def enqueue(self, patient):
        with self._lock:
            self._queues[patient.triage_level].append(patient)

    def dequeue(self):
        with self._lock:
            for level in (1, 2, 3):
                if self._queues[level]:
                    return self._queues[level].popleft()
            raise EmptyQueueError("...")
```

Para procesos en distintas máquinas haría falta un almacén compartido (Redis, base de datos) con transacciones; el principio es el mismo: una sola mutación de estado a la vez por paciente.
