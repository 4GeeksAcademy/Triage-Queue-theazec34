"""Sistema de cola de triaje para urgencias hospitalarias."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, Dict, List, Optional


@dataclass
class Patient:
    """Paciente en espera de atención."""

    name: str
    triage_level: int
    arrived_at: datetime

    def __post_init__(self) -> None:
        if self.triage_level not in (1, 2, 3):
            raise ValueError("El nivel de triaje debe ser 1, 2 o 3.")

    def __str__(self) -> str:
        return (
            f"{self.name} | Nivel {self.triage_level} | "
            f"Llegada: {self.arrived_at.strftime('%H:%M:%S')}"
        )


class EmptyQueueError(Exception):
    """Se lanza cuando se intenta operar sobre una cola vacía."""


class TriageQueue:
    """Cola de prioridad con tres niveles de triaje (1 > 2 > 3, FIFO por nivel)."""

    def __init__(self) -> None:
        self._queues: Dict[int, Deque[Patient]] = {
            1: deque(),
            2: deque(),
            3: deque(),
        }

    def enqueue(self, patient: Patient) -> None:
        """Encola un paciente respetando prioridad y orden de llegada."""
        self._queues[patient.triage_level].append(patient)

    def _next_level_with_patients(self) -> Optional[int]:
        for level in (1, 2, 3):
            if self._queues[level]:
                return level
        return None

    def dequeue(self) -> Patient:
        """Desencola y devuelve al siguiente paciente a atender."""
        level = self._next_level_with_patients()
        if level is None:
            raise EmptyQueueError("No hay pacientes en la cola de espera.")
        return self._queues[level].popleft()

    def peek(self) -> Patient:
        """Devuelve el siguiente paciente sin removerlo de la cola."""
        level = self._next_level_with_patients()
        if level is None:
            raise EmptyQueueError("No hay pacientes en la cola de espera.")
        return self._queues[level][0]

    def list_queue(self) -> List[Patient]:
        """Lista todos los pacientes en el orden en que serán atendidos."""
        result: List[Patient] = []
        for level in (1, 2, 3):
            result.extend(self._queues[level])
        return result

    def stats(self) -> Dict[int, int]:
        """Devuelve cuántos pacientes hay en cada nivel de triaje."""
        return {level: len(self._queues[level]) for level in (1, 2, 3)}


def _read_non_empty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("El valor no puede estar vacío. Inténtalo de nuevo.")


def _read_triage_level() -> int:
    while True:
        raw = input("Nivel de triaje (1=Crítico, 2=Urgente, 3=Estándar): ").strip()
        if raw in {"1", "2", "3"}:
            return int(raw)
        print("Nivel inválido. Debe ser 1, 2 o 3.")


def _print_queue(queue: TriageQueue) -> None:
    patients = queue.list_queue()
    if not patients:
        print("\nLa cola está vacía.\n")
        return
    print("\nCola de espera (orden de atención):")
    for index, patient in enumerate(patients, start=1):
        print(f"  {index}. {patient}")
    print()


def _print_stats(queue: TriageQueue) -> None:
    stats = queue.stats()
    print("\nEstadísticas de la cola:")
    print(f"  Nivel 1 (Crítico):  {stats[1]}")
    print(f"  Nivel 2 (Urgente):  {stats[2]}")
    print(f"  Nivel 3 (Estándar): {stats[3]}")
    print(f"  Total:              {sum(stats.values())}\n")


def run_cli() -> None:
    """Menú interactivo en español para operar la cola de triaje."""
    queue = TriageQueue()

    while True:
        print("=== Sistema de Triaje — Urgencias ===")
        print("1. Encolar paciente")
        print("2. Desencolar (llamar siguiente)")
        print("3. Ver siguiente paciente (peek)")
        print("4. Listar cola")
        print("5. Estadísticas")
        print("6. Salir")

        option = input("Selecciona una opción (1-6): ").strip()

        if option == "1":
            name = _read_non_empty_string("Nombre del paciente: ")
            level = _read_triage_level()
            patient = Patient(name=name, triage_level=level, arrived_at=datetime.now())
            queue.enqueue(patient)
            print(f"\nPaciente encolado: {patient}\n")

        elif option == "2":
            try:
                patient = queue.dequeue()
                print(f"\nSiguiente paciente llamado: {patient}\n")
            except EmptyQueueError as exc:
                print(f"\n{exc}\n")

        elif option == "3":
            try:
                patient = queue.peek()
                print(f"\nSiguiente en la cola: {patient}\n")
            except EmptyQueueError as exc:
                print(f"\n{exc}\n")

        elif option == "4":
            _print_queue(queue)

        elif option == "5":
            _print_stats(queue)

        elif option == "6":
            print("\nSaliendo del sistema. ¡Hasta pronto!\n")
            break

        else:
            print("\nOpción inválida. Elige un número del 1 al 6.\n")


if __name__ == "__main__":
    run_cli()
