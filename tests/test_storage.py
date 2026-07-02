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

