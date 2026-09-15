import argparse
from collections.abc import Callable
from rich.console import Console

from .todo import (
    add_task,
    add_subtask,
    complete_task,
    complete_subtask,
    list_tasks,
    remove_task,
    remove_subtask,
    Task,
)

console = Console()

DEFAULT_FILENAME = "TODO.md"


def parse_add_arguments(
    file_or_task: str,
    task: str | None,
) -> tuple[str, str]:
    if task is None:
        return DEFAULT_FILENAME, file_or_task

    return file_or_task, task


def parse_task_reference(
    file_or_reference: str,
    reference: str | None,
) -> tuple[str, int, int | None]:
    if reference is None:
        filename = DEFAULT_FILENAME
        value = file_or_reference
    else:
        filename = file_or_reference
        value = reference

    parts = value.split(".")

    if len(parts) == 1:
        try:
            return filename, int(parts[0]), None
        except ValueError as error:
            raise ValueError(
                "expected a task number or a task.subtask reference"
            ) from error

    if len(parts) == 2:
        try:
            return filename, int(parts[0]), int(parts[1])
        except ValueError as error:
            raise ValueError(
                "expected a task number or a task.subtask reference"
            ) from error

    raise ValueError(
        "expected a task number or a task.subtask reference"
    )


def handle_add(args: argparse.Namespace) -> None:
    filename, task = parse_add_arguments(
        args.file_or_task,
        args.task,
    )

    add_task(filename, task)

    print(f"Added: {task}")
    print(f"File: {filename}")


def handle_add_subtasks(args: argparse.Namespace) -> None:
    filename = args.filename
    task_index = args.task_index
    description = args.description

    add_subtask(filename, task_index, description)

    print(
        f"Added subtask to task {task_index}: "
        f"{description}"
        )


def display_task(
        index: int,
        task: Task,
        style: str,
        ) -> None:
    status = "X" if task.completed else " "

    console.print(
        f"{index}. [{status}] {task.description}", style=style
    )

    for sub_index, subtask in enumerate(task.subtasks, start=1,):
        status = "X" if subtask.completed else " "
        style = "green" if subtask.completed else "orange1"

        console.print(
            f"    {sub_index}. [{status}] "
            f"{subtask.description}",
            style=style,
        )


def handle_list(args: argparse.Namespace) -> None:
    tasks = list_tasks(args.filename)

    if not tasks:
        print("No tasks scheluded.")
        return

    for index, task in enumerate(tasks, start=1):
        if args.pending and task.completed:
            continue

        if args.completed and not task.completed:
            continue

        style = "green" if task.completed else "orange1"

        display_task(index, task, style)


def handle_done(args: argparse.Namespace) -> None:
    filename, task_index, subtask_index = parse_task_reference(
        args.file_or_reference,
        args.reference,
    )

    if subtask_index is None:
        complete_task(filename, task_index)
        print(f"Completed task {task_index}.")
        return

    complete_subtask(filename, task_index, subtask_index,)

    print(f"Completed subtask {task_index}.{subtask_index}.")


def handle_remove(args: argparse.Namespace) -> None:
    filename, task_index, subtask_index = parse_task_reference(
        args.file_or_reference,
        args.reference,
    )

    if subtask_index is None:
        remove_task(filename, task_index)
        print(f"Removed task {task_index}.")
        return

    remove_subtask(filename, task_index, subtask_index)

    print(f"Removed subtask {task_index}.{subtask_index}.")


HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "add": handle_add,
    "add-subtask": handle_add_subtasks,
    "list": handle_list,
    "done": handle_done,
    "remove": handle_remove,
}


def build_parser() -> argparse.ArgumentParser:
    # COMMAND LINE PARSER
    parser = argparse.ArgumentParser(
        prog="todolist",
        description="A simple command-line todo list.",
    )

    # COMMAND PARSER
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # ADD PARSER
    add_parser = subparsers.add_parser(
        "add",
        help="Add a task to a todo file.",
    )

    add_parser.add_argument(
        "file_or_task",
        help="Task or path to the todo file.",
    )

    add_parser.add_argument(
        "task",
        nargs="?",
        help="Task to add.",
    )

    add_subtask_parser = subparsers.add_parser(
        "add-subtask",
        help="Add a subtask to a task.",
    )

    add_subtask_parser.add_argument(
        "task_index",
        type=int,
        help="Task number.",
    )

    add_subtask_parser.add_argument(
        "description",
        help="Subtask description.",
    )

    add_subtask_parser.add_argument(
        "--file",
        dest="filename",
        default=DEFAULT_FILENAME,
        help="Path to the todo file.",
    )


    # LIST PARSER
    list_parser = subparsers.add_parser(
        "list",
        help="List tasks from a todo file.",
    )

    list_parser.add_argument(
        "filename",
        nargs="?",
        default=DEFAULT_FILENAME,
        help="Path to the todo file (default: TODO.md).",
    )

    list_parser.add_argument(
        "--pending",
        action="store_true",
        help="Show only pending tasks.",
    )


    list_parser.add_argument(
        "--completed",
        action="store_true",
        help="Show only completed tasks.",
    )


    # DONE PARSER
    done_parser = subparsers.add_parser(
        "done",
        help="Mark a task as completed.",
    )

    done_parser.add_argument(
        "file_or_reference",
        help="Task reference or path to the todo file.",
    )

    done_parser.add_argument(
        "reference",
        nargs="?",
        help="Task number or task.subtask reference.",
    )

    # REMOVE PARSER
    remove_parser = subparsers.add_parser(
        "remove",
        help="Remove a task.",
    )

    remove_parser.add_argument(
        "file_or_reference",
        help="Task reference or path to the todo file.",
    )

    remove_parser.add_argument(
        "reference",
        nargs="?",
        help="Task number.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    handler = HANDLERS[args.command]

    try:
        handler(args)
    except (OSError, IndexError, ValueError) as error:
        parser.error(str(error))
