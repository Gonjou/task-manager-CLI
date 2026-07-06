import pytest
import json
from tasks.storage import TaskManager

@pytest.fixture
def manager(tmp_path):
    return TaskManager(
        tasks_file=tmp_path / "tasks.json",
        settings_file=tmp_path / "settings.json"
    )


@pytest.fixture
def sample_tasks():
    return [
  {
    "title": "sweep floor",
    "description": "room",
    "due_date": "2000-08-06",
    "completed": False,
    "today": True,
    "this_week": False
  },
  {
    "title": "do homework",
    "description": "math and sciences",
    "due_date": "2001-09-09",
    "completed": True,
    "today": False,
    "this_week": True
  }]


def test_load_tasks_returns_empty_list_when_file_doesnt_exist(manager):
    assert manager.load_tasks() == []


def test_save_and_load_tasks(manager, sample_tasks):
    manager.save_tasks(sample_tasks)

    assert manager.load_tasks() == sample_tasks


def test_load_settings_uses_default_when_file_doesnt_exist(manager):
    assert manager.load_settings() == {"display_tasks_at_launch": True}


def test_load_settings_and_save_settings(manager):
    manager.save_settings({"display_tasks_at_launch": False})

    assert manager.load_settings() == {"display_tasks_at_launch": False}


def test_load_tasks_reads_existing_json_file(tmp_path):
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text(json.dumps([{"title": "Example task"}]))
    manager = TaskManager(tasks_file=tasks_file)

    assert manager.load_tasks() == [{"title": "Example task"}]


def test_load_settings_reads_existing_json_file(tmp_path):
    settings_file = tmp_path / "settings.json"
    settings_file.write_text(json.dumps({"display_tasks_at_launch": False}))
    manager = TaskManager(settings_file=settings_file)

    assert manager.load_settings() == {"display_tasks_at_launch": False}


@pytest.mark.parametrize(
        "index, error_type, message",
        [
            ("abc", ValueError, "Task index must be a number."),
            ("0", ValueError, "Index must be greater than 0."),
            ("4", IndexError, "This task does not exist."),
        ]
        )

def test_validate_index_rejects_invalid_values(manager, sample_tasks, index, error_type, message):
    with pytest.raises(error_type, match=message):
        manager.validate_index(index, sample_tasks)


@pytest.mark.parametrize(
    "index, expected",
    [
        ("1", 1),
        ("2", 2),
    ]
)

def test_validate_index_accepts_existing_values(manager, sample_tasks, index, expected):
    assert manager.validate_index(index, sample_tasks) == expected


@pytest.mark.parametrize(
    "title, expected",
    [
        ("Sweep floor", "Sweep floor"),
        ("   do homework   ", "do homework"),
    ]
)

def test_validate_title_accepts_valid_title(manager, title, expected):
    assert manager.validate_title(title) == expected


def test_validate_title_rejects_empty_title(manager):
    with pytest.raises(ValueError, match="Title cannot be empty"):
        manager.validate_title("   ")


@pytest.mark.parametrize(
        "due_date", ["3rd of July 2026", "2026-13-07", "13-02-2026"]
)

def test_validate_due_date_rejects_invalid_date_formats(manager, due_date):
    with pytest.raises(ValueError, match="Invalid date format"):
        manager.validate_due_date(due_date)


def test_validate_due_date_accepts_yyyymmdd_date(manager):
    assert manager.validate_due_date("2026-07-03") == "2026-07-03"


def test_add_task_adds_task_to_list(manager, sample_tasks):
    manager.add_task(sample_tasks, "study science", "", "2026-07-04")
    manager.save_tasks(sample_tasks)

    assert manager.load_tasks() == sample_tasks


def test_list_tasks_returns_display_rows(manager, sample_tasks):
    assert manager.list_tasks(sample_tasks) == [
        [1, "sweep floor", "2000-08-06", "Incomplete"],
        [2, "do homework", "2001-09-09", "Completed"]
    ]

def test_sort_option_rejects_invalid_choices(manager):
    with pytest.raises(ValueError):
        manager.validate_sort_option("6")


@pytest.mark.parametrize("choice", ["1", "2", "3", "4", "5"])
def test_sort_option_accepts_valid_choices(manager, choice):
    assert manager.validate_sort_option(choice) == choice


def test_sort_tasks_sort_by_title(manager, sample_tasks):
    sorted_tasks = manager.sort_tasks(sample_tasks, "title")

    assert sorted_tasks[0]["title"] == "do homework"

def test_sort_tasks_by_due_date(manager, sample_tasks):
    sorted_tasks = manager.sort_tasks(sample_tasks, "due date")

    assert sorted_tasks[0]["title"] == "sweep floor"


def test_sort_tasks_by_due_date_reversed(manager, sample_tasks):
    sorted_tasks = manager.sort_tasks(sample_tasks, "due date", reverse=True)

    assert sorted_tasks[0]["title"] == "do homework"

def test_sort_tasks_by_completion(manager, sample_tasks):
    sorted_tasks = manager.sort_tasks(sample_tasks, "completion")

    assert sorted_tasks[0]["title"] == "sweep floor"

def test_assign_tasks_for_today(manager, sample_tasks):
    manager.assign_tasks(sample_tasks, 2, "1")
    manager.save_tasks(sample_tasks)

    assert [task["today"] for task in sample_tasks] == [True, True]

def test_assign_tasks_for_this_week(manager, sample_tasks):
    manager.assign_tasks(sample_tasks, 1, "2")
    manager.save_tasks(sample_tasks)

    assert [task["this_week"] for task in sample_tasks] == [True, True]

def test_unassign_tasks_for_today(manager, sample_tasks):
    manager.assign_tasks(sample_tasks, 1, "3")
    manager.save_tasks(sample_tasks)

    assert [task["today"] for task in sample_tasks] == [False, False]

def test_unassign_tasks_for_this_week(manager, sample_tasks):
    manager.assign_tasks(sample_tasks, 2, "4")
    manager.save_tasks(sample_tasks)

    assert [task["this_week"] for task in sample_tasks] == [False, False]

def test_delete_task(manager, sample_tasks):
    manager.delete_task(sample_tasks, "2")
    manager.save_tasks(sample_tasks)

    assert len(sample_tasks) == 1

def test_search_task(manager, sample_tasks):
    task = manager.search_task(sample_tasks, "2")
    assert task["title"] == "do homework"

def test_mark_as_completed(manager, sample_tasks):
    manager.mark_as_completed(sample_tasks, "1")
    manager.save_tasks(sample_tasks)

    assert sample_tasks[0]["completed"] == True

def test_mark_as_incomplete(manager, sample_tasks):
    manager.mark_as_incomplete(sample_tasks, "2")
    manager.save_tasks(sample_tasks)

    assert sample_tasks[1]["completed"] == False
