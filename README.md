## Installation

#### Requirements:
- Python >= 3.12
- pip

## Basic Usage:

Clone the repository, then run:
```
python3 -m pip install .
```

To see all features:
```
todolist --help
```

| Key | Description | Syntax | Example |
|-----|-------------|--------|---------|
| todolist | The program name |   |   |
| add | Adds a task | "task" |todolist add "Write a README" |
| add | Adds a task with one or moresubtasks | "task -- subtask" | todolist add "Write a README -- re-write the Installation section" |
| add-subtask | Adds a subtask to a task | task_index "task" | todolist add-subtask 1 "re-write the Resources section" |
| done | Marks a task as "completed" | task_index | todolist done 1 |
| done | Marks a subtask as "completed" | task_index.subtask_index | todolist done 1.1 |
| undone | Marks a task as "undone" | task_index | todolist undone 1 |
| undone | Marks a subtask as "undone" | task_index.subtask_index | todolist undone 1.1 |
| remove | Removes a task from the todolist | task_index | todolist remove 1 |
| remove | Removes a subtask from a task | task_index.subtask_index | todolist remove 1.1 |
| list | Displays the todolist tasks |   | todolist list |




To add a task:
```
todolist add "your_task"
```

To add a task with subtask(s):
```
todolist add "your_task -- your_subtask1 -- your_subtask2"
```
The syntax for a subtask is "```(space)--(space)```"

To add a subtask to an already existing task:
```
todolist add-subtask 1 "your_subtask"
```
For example:
```
todolist add "Shoppping List"
todolist list

1. [ ] Shopping List

todolist add-subtask 1 "Tomatoes"
todolist list

1. [ ] Shopping List
    1. [ ] Tomatoes
```

To mark a task as ```completed```
```
todolist done task_index
```

Or mark a subtask as ```completed```:
```
todolist done task_index.subtask_index
```

For example:
```
todolist done 1
```
Will mark the **first task** as ```completed```
```
todolist done 1.1
```
Will mark the **first subtask** of the first task as ```completed```

To remove a task:
```
todolist remove task_index
```

To remove a subtask:
```
todolist remove task_index.subtask_index
```

To display the task list:
```
todolist list
```

## v0.2.0

Added an auto-complete subtasks when the main task is marked as done

Added undone feature

To mark a task as ```undone```
```
todolist undone task_index
```

To mark a subtask as ```undone```
```
todolist undone task_index.subtask_index
```
task_index = 1, 2, 3...
task_index.subtask_index = 1.1, 1.2, 2.1...
