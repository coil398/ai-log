# 記録と同期

日次ログの追記またはトピックノート追加のときだけ読む。

## 前提

- データ根: `~/ai-log-data`
- タイムゾーン: Asia/Tokyo
- 触ったファイルだけを stage する（`git add -A` は使わない）
- 出所: **`<host>-<bot>`**（ファイル名・front matter・commit に載せる）

## 日次ログの追記

1. 最新化

```bash
git -C ~/ai-log-data pull --rebase
```

2. パスを決める

```bash
DATE=$(TZ=Asia/Tokyo date +%Y-%m-%d)
HOST=<host>   # e.g. hermes
BOT=<bot>     # e.g. main
FILE=~/ai-log-data/daily/$DATE/${HOST}-${BOT}.md
mkdir -p ~/ai-log-data/daily/$DATE
```

3. ファイルが無ければ front matter（`date` / `host` / `bot` / `agent: <host>-<bot>` / `type: daily-work-log`）付きで新規作成。あれば末尾に追記:

```markdown
---

## HH:MM JST <title>

（本文）
```

4. 補助 script（推奨）:

```bash
python3 "$SKILL_DIR/scripts/new_entry.py" \
  --repo ~/ai-log-data \
  --host "$HOST" \
  --bot "$BOT" \
  --title "<title>" \
  --body "<body>"
```

script は pull → 書き込み → 触ったファイルだけ add/commit → push まで行う。`--no-commit` / `--no-push` で段階を止められる。

## commitメッセージ

- 日次・トピック: `log(<host>): YYYY-MM-DD <summary>`
- タスク: `task(<host>): <id> <summary>`（[tasks.md](tasks.md)）
- ハンドオフ: `handoff(<host>): YYYY-MM-DD <summary>`（[handoff.md](handoff.md)）
- ドキュメント: `docs(<host>): <summary>`

## 手動で commit / push する場合

```bash
git -C ~/ai-log-data add -- "daily/$DATE/${HOST}-${BOT}.md"
git -C ~/ai-log-data commit -m "log($HOST): $DATE <summary>"
git -C ~/ai-log-data push
```

## 失敗時

- pull / rebase が失敗したら、勝手に resolve せず原因を報告する
- push が失敗したら local commit は残し、原因を報告する
- dirty な無関係ファイルがあっても `git add -A` で巻き込まない
