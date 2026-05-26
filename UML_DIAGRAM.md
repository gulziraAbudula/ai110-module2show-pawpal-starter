# PawPal+ UML Class Diagram (Updated)

```mermaid
classDiagram
    class Owner {
        -name: str
        -email: str
        -available_hours: int
        +__init__(name, email, available_hours)
        +get_name() str
        +set_name(name: str) None
        +get_email() str
        +set_email(email: str) None
        +get_available_hours() int
        +set_available_hours(hours: int) None
    }

    class Pet {
        -name: str
        -age: int
        -breed: str
        -owner: Owner
        +__init__(name, age, breed, owner)
        +get_name() str
        +set_name(name: str) None
        +get_age() int
        +set_age(age: int) None
        +get_breed() str
        +set_breed(breed: str) None
    }

    class Task {
        -title: str
        -task_type: str
        -frequency: str
        -duration: int
        -priority: int
        -is_completed: bool
        -time: Optional~time~
        -due_date: Optional~date~
        -pet: Pet
        +__init__(title, task_type, frequency, duration, priority, time, due_date, is_completed, pet)
        +__hash__() int
        +get_title() str
        +set_title(title: str) None
        +get_task_type() str
        +set_task_type(task_type: str) None
        +get_duration() int
        +set_duration(duration: int) None
        +get_priority() int
        +set_priority(priority: int) None
        +get_frequency() str
        +set_frequency(frequency: str) None
        +mark_completed() None
        +get_completion_status() bool
    }

    class DailySchedule {
        -tasks: List~Task~
        -scheduled_tasks: Dict~Task, int~
        +__init__(tasks, scheduled_tasks)
        +add_task(task: Task) None
        +schedule(owner: Owner, pets: List~Pet~) Dict~Task, int~
        +validate() bool
        +get_validation_errors() List~str~
        +explain() str
        +get_scheduled_tasks() Dict~Task, int~
        +filter_tasks(is_completed: Optional~bool~, pet_name: Optional~str~) List~Task~
        +detect_scheduling_conflicts() List~str~
        +mark_task_complete(task: Task) Optional~Task~
    }

    Pet "*" --> "1" Owner : belongs to
    DailySchedule "1" --> "*" Task : contains
    Task --> Pet : schedules for
    DailySchedule --> Owner : uses
```

## Key Updates from Original UML

### Task Class Enhancements
- **Added attributes:**
  - `time: Optional[time]` — preferred task start time for scheduling
  - `due_date: Optional[date]` — task due date for recurring task tracking
  
- **Added methods:**
  - `__hash__()` — makes Task hashable for use as dictionary key in scheduled_tasks

### DailySchedule Class Enhancements
- **New methods:**
  - `add_task(task: Task)` — adds task to schedule (core operation)
  - `filter_tasks(is_completed, pet_name)` — filter tasks by completion status and/or pet name
  - `detect_scheduling_conflicts()` — returns list of conflict warnings for overlapping tasks
  - `mark_task_complete(task: Task)` — marks task complete and creates next occurrence for recurring tasks
  - `get_validation_errors()` — returns detailed list of validation errors instead of just boolean
  
- **Updated methods:**
  - `validate()` — now uses get_validation_errors() internally

## Architecture

**Relationships:**
- Pet has a 1:1 relationship with Owner (many pets can belong to one owner)
- DailySchedule contains many Tasks (1:*)
- Task is associated with one Pet
- DailySchedule uses Owner's available_hours for constraint-based scheduling

**Key Features Supported:**
- Multi-tier sorting (time, frequency, priority)
- Recurring task management (daily/weekly auto-recurrence)
- Conflict detection (same-time and same-pet conflicts)
- Task filtering (by status and pet)
- Schedule validation (critical tasks checking)
- Constraint-based optimization (respects available hours)
