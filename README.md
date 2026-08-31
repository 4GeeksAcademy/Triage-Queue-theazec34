# Triage-Queue-theazec34

Informacion basica sobre el proyecto:

Qué incluye
triage_queue.py

Clase Patient con name, triage_level (1–3) y arrived_at
Clase TriageQueue con las 5 operaciones: enqueue, dequeue, peek, list_queue, stats
Menú CLI en español con validación de entradas y manejo de cola vacía
DESIGN.md

Por qué se usan 3 colas deque (una por nivel) en lugar de un solo deque, lista ordenada o heapq
Cómo manejar concurrencia con candados para evitar doble procesamiento
README.md

Instrucciones de ejecución y estructura del proyecto
Lógica de prioridad
Nivel 1 siempre antes que 2, y 2 antes que 3
Dentro del mismo nivel: orden de llegada (FIFO)
enqueue y dequeue en O(1) gracias a las tres colas separadas
