from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_FILE = Path(".todo-data.json")


def load_tasks(data_file: Path = DATA_FILE) -> list[dict[str, object]]:
    if not data_file.exists():
        return []

    with data_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks: list[dict[str, object]], data_file: Path = DATA_FILE) -> None:
    with data_file.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


def add_task(title: str, data_file: Path = DATA_FILE) -> dict[str, object]:
    tasks = load_tasks(data_file)
    next_id = max((int(task["id"]) for task in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    save_tasks(tasks, data_file)
    return task


def list_tasks(data_file: Path = DATA_FILE) -> list[dict[str, object]]:
    return load_tasks(data_file)


def complete_task(task_id: int, data_file: Path = DATA_FILE) -> dict[str, object]:
    tasks = load_tasks(data_file)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks, data_file)
            return task

    raise ValueError(f"{task_id}번 할 일을 찾을 수 없습니다.")


def delete_task(task_id: int, data_file: Path = DATA_FILE) -> dict[str, object]:
    tasks = load_tasks(data_file)

    for task in tasks:
        if task["id"] == task_id:
            remaining_tasks = [item for item in tasks if item["id"] != task_id]
            save_tasks(remaining_tasks, data_file)
            return task

    raise ValueError(f"{task_id}번 할 일을 찾을 수 없습니다.")


def clear_completed(data_file: Path = DATA_FILE) -> int:
    tasks = load_tasks(data_file)
    remaining_tasks = [task for task in tasks if not task["done"]]
    removed_count = len(tasks) - len(remaining_tasks)
    save_tasks(remaining_tasks, data_file)
    return removed_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="간단한 CLI TODO 프로그램")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="할 일을 추가합니다.")
    add_parser.add_argument("title", help="추가할 할 일 제목")

    subparsers.add_parser("list", help="할 일 목록을 조회합니다.")

    done_parser = subparsers.add_parser("done", help="할 일을 완료 처리합니다.")
    done_parser.add_argument("task_id", type=int, help="완료할 할 일 번호")

    delete_parser = subparsers.add_parser("delete", help="할 일을 삭제합니다.")
    delete_parser.add_argument("task_id", type=int, help="삭제할 할 일 번호")

    clear_parser = subparsers.add_parser("clear", help="완료된 할 일을 정리합니다.")
    clear_parser.add_argument(
        "--done",
        action="store_true",
        help="완료된 항목만 모두 삭제합니다.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "add":
            task = add_task(args.title)
            print(f"[추가] {task['id']}. {task['title']}")
            return 0

        if args.command == "list":
            tasks = list_tasks()
            if not tasks:
                print("등록된 할 일이 없습니다.")
                return 0

            for task in tasks:
                status = "완료" if task["done"] else "진행중"
                print(f"{task['id']}. [{status}] {task['title']}")
            return 0

        if args.command == "done":
            task = complete_task(args.task_id)
            print(f"[완료] {task['id']}. {task['title']}")
            return 0

        if args.command == "delete":
            task = delete_task(args.task_id)
            print(f"[삭제] {task['id']}. {task['title']}")
            return 0

        if args.command == "clear":
            if not args.done:
                parser.error("`clear` 명령은 `--done` 옵션과 함께 사용해야 합니다.")
            removed_count = clear_completed()
            print(f"[정리] 완료된 항목 {removed_count}개를 삭제했습니다.")
            return 0
    except ValueError as error:
        print(f"오류: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
