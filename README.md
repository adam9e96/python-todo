# Python TODO

`uv`로 실행하는 간단한 CLI TODO 프로그램입니다.

## 실행 방법

```bash
uv run todo add "장보기"
uv run todo list
uv run todo done 1
uv run todo delete 1
uv run todo clear --done
```

## 지원 기능

- 할 일 추가
- 할 일 목록 조회
- 할 일 완료 처리
- 할 일 삭제
- 완료된 항목 일괄 정리

기본 데이터 파일은 프로젝트 루트의 `.todo-data.json` 입니다.
