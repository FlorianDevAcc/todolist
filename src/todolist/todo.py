#!/usr/bin/env python3


from dataclasses import dataclass
from pathlib import Path


@dataclass
class Task:
    description: str
    completed: bool = False


def parse_task(line: str) -> Task:
    line = line.rstrip("\n")

    if line.startswith("[X] "):
        return Task(line[4:], completed=True)

    if line.startswith("[ ] "):
        return Task(line[4:], completed=False)

    raise ValueError(f"Invalid task format: {line}")


def format_task(task: Task) -> str:
    status = "X" if task.completed else " "
    return f"[{status}] {task.description}"


def add_task(filename: str, description: str) -> None:
    if not description.strip():
        raise ValueError("Task cannot be empty.")

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    task = Task(description)

    with path.open("a", encoding="utf-8") as file:
        file.write(format_task(task) + "\n")


def save_tasks(filename: str, tasks: list[Task]) -> None:
    path = Path(filename)

    with path.open("w", encoding="utf-8") as file:
        for task in tasks:
            file.write(format_task(task) + "\n")


def complete_task(filename: str, index: int) -> None:
    tasks = list_tasks(filename)

    if index < 1 or index > len(tasks):
        raise IndexError("task index out of range")

    tasks[index - 1].completed = True

    save_tasks(filename, tasks)


def remove_task(filename: str, index: int) -> None:
    tasks = list_tasks(filename)

    if index < 1 or index > len(tasks):
        raise IndexError("task index out of range")

    tasks.pop(index -1)

    save_tasks(filename, tasks)


def list_tasks(filename: str) -> list[Task]:
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(filename)

    with path.open("r", encoding="utf-8") as file:
        return [parse_task(line) for line in file if line.strip()]



