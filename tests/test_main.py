import tempfile
import unittest
from pathlib import Path

from python_todo.cli import (
    add_task,
    clear_completed,
    complete_task,
    delete_task,
    list_tasks,
)


class TodoCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "tasks.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_task(self) -> None:
        task = add_task("공부하기", self.data_file)
        tasks = list_tasks(self.data_file)

        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "공부하기")
        self.assertFalse(task["done"])
        self.assertEqual(len(tasks), 1)

    def test_complete_task(self) -> None:
        task = add_task("운동하기", self.data_file)

        updated = complete_task(task["id"], self.data_file)

        self.assertTrue(updated["done"])
        self.assertTrue(list_tasks(self.data_file)[0]["done"])

    def test_delete_task(self) -> None:
        first = add_task("책 읽기", self.data_file)
        add_task("정리하기", self.data_file)

        deleted = delete_task(first["id"], self.data_file)
        tasks = list_tasks(self.data_file)

        self.assertEqual(deleted["title"], "책 읽기")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "정리하기")

    def test_clear_completed(self) -> None:
        first = add_task("메일 보내기", self.data_file)
        add_task("회의 준비", self.data_file)
        complete_task(first["id"], self.data_file)

        removed_count = clear_completed(self.data_file)
        tasks = list_tasks(self.data_file)

        self.assertEqual(removed_count, 1)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "회의 준비")


if __name__ == "__main__":
    unittest.main()
