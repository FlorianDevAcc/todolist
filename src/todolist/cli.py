import argparse
from collections.abc import Callable
from rich.console import Console

from .todo import (
    add_task,
    complete_task,
    format_task,
    list_tasks,
    remove_task,
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
    file_or_index: str,
    index: int | None,
) -> tuple[str, int]:
    if index is None:
        try:
            return DEFAULT_FILENAME, int(file_or_index)
        except ValueError as error:
            raise ValueError(
                "expected a task number or a filename followed "
                "by a task number"
            ) from error

    return file_or_index, index


def handle_add(args: argparse.Namespace) -> None:
    filename, task = parse_add_arguments(
        args.file_or_task,
        args.task,
    )

    add_task(filename, task)

    print(f"Added: {task}")
    print(f"File: {filename}")


def handle_list(args: argparse.Namespace) -> None:
    tasks = list_tasks(args.filename)

    for index, task in enumerate(tasks, start=1):
        if args.pending and task.completed:
            continue

        if args.completed and not task.completed:
            continue

        style = "green" if task.completed else "orange1"

        console.print(f"{index}. {format_task(task)}", style=style)


def handle_done(args: argparse.Namespace) -> None:
    filename, index = parse_task_reference(
        args.file_or_index,
        args.index,
    )

    complete_task(filename, index)

    print(f"Completed task {index}.")


def handle_remove(args: argparse.Namespace) -> None:
    filename, index = parse_task_reference(
        args.file_or_index,
        args.index,
    )

    remove_task(filename, index)

    print(f"Removed task {index}.")


HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "add": handle_add,
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
        "file_or_index",
        help="Task number or path to the todo file.",
    )

    done_parser.add_argument(
        "index",
        nargs="?",
        type=int,
        help="Task number.",
    )

    # REMOVE PARSER
    remove_parser = subparsers.add_parser(
        "remove",
        help="Remove a task.",
    )

    remove_parser.add_argument(
        "file_or_index",
        help="Task number or path to the todo file.",
    )

    remove_parser.add_argument(
        "index",
        nargs="?",
        type=int,
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
