#!/usr/bin/env python3


from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SubTask:
    description: str
    completed: bool = False

@dataclass
class Task:
    description: str
    completed: bool = False
    subtasks: list[SubTask] = field(default_factory=list)


def parse_task(line: str) -> Task:
    line = line.rstrip("\n")

    parts = [part.strip() for part in line.split(" -- ")]

    if not parts:
        raise ValueError(f"Invalid task format: {line}")

    main = parts[0]

    if main.startswith("[X] "):
        task = Task(main[4:], completed=True)
    elif main.startswith("[ ] "):
        task = Task(main[4:], completed=False)
    else:
        raise ValueError(f"Invalid task format: {line}")

    for part in parts[1:]:
        if part.startswith("[X] "):
            task.subtasks.append(
                SubTask(part[4:], completed=True)
            )
        elif part.startswith("[ ] "):
            task.subtasks.append(
                SubTask(part[4:], completed=False)
            )
        elif part:
            task.subtasks.append(
                SubTask(part, completed=False)
            )

    return task


def format_task(task: Task) -> str:
    status = "X" if task.completed else " "

    parts = [
        f"[{status}] {task.description}"
    ]

    for subtask in task.subtasks:
        status = "X" if subtask.completed else " "
        parts.append(f"[{status}] {subtask.description}")

    return " -- ".join(parts)


def add_task(filename: str, description: str) -> None:
    if not description.strip():
        raise ValueError("Task cannot be empty.")

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    task = Task(description)

    with path.open("a", encoding="utf-8") as file:
        file.write(format_task(task) + "\n")


def add_subtask(filename: str, task_index: int, description: str) -> None:
    if not description.strip():
        raise ValueError("Task cannot be empty.")

    tasks = list_tasks(filename)

    if task_index < 1 or task_index > len(tasks):
        raise IndexError("Task index out of range")

    task = tasks[task_index - 1]
    task.subtasks.append(SubTask(description))

    save_tasks(filename, tasks)

def list_tasks(filename: str) -> list[Task]:
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(filename)

    with path.open("r", encoding="utf-8") as file:
        return [parse_task(line) for line in file if line.strip()]


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


def complete_subtask(filename: str, task_index: int, subtask_index: int) -> None:
    tasks = list_tasks(filename)

    if task_index < 1 or task_index > len(tasks):
        raise IndexError("Task index out of range")

    task = tasks[task_index - 1]

    if subtask_index < 1 or subtask_index > len(task.subtasks):
        raise IndexError("Subtask index out of range")

    task.subtasks[subtask_index - 1].completed = True

    save_tasks(filename, tasks)


def remove_task(filename: str, index: int) -> None:
    tasks = list_tasks(filename)

    if index < 1 or index > len(tasks):
        raise IndexError("Task index out of range")

    tasks.pop(index - 1)

    save_tasks(filename, tasks)


def remove_subtask(filename: str, task_index: int, subtask_index: int,) -> None:
    tasks = list_tasks(filename)

    if task_index < 1 or task_index > len(tasks):
        raise IndexError("Task index out of range")

    task = tasks[task_index - 1]

    if subtask_index < 1 or subtask_index > len(task.subtasks):
        raise IndexError("Subtask index out of range")

    task.subtasks.pop(subtask_index - 1)

    save_tasks(filename, tasks)


