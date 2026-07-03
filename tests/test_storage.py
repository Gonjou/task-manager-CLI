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
