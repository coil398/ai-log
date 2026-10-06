# 記録と同期

日次ログの追記またはトピックノート追加のときだけ読む。

## 前提

- データ根: `~/ai-log-data`
- タイムゾーン: Asia/Tokyo
- 触ったファイルだけを stage する（`git add -A` は使わない）

## 日次ログの追記

1. 最新化

```bash
git -C ~/ai-log-data pull --rebase
```

2. パスを決める

```bash
DATE=$(TZ=Asia/Tokyo date +%Y-%m-%d)
TIME=$(TZ=Asia/Tokyo date +%H:%M)
AGENT=<agent-name>
FILE=~/ai-log-data/daily/$DATE/$AGENT.md
mkdir -p ~/ai-log-data/daily/$DATE
```

3. ファイルが無ければ front matter 付きで新規作成。あれば末尾に追記:

```markdown
---

## HH:MM JST <title>

（本文）
```

4. 補助scriptを使う場合（推奨）:

```bash
python3 "$SKILL_DIR/scripts/new_entry.py" \
  --repo ~/ai-log-data \
  --agent "$AGENT" \
  --title "<title>" \
  --body "<body>"
```

scriptは pull → 書き込み → 触ったファイルだけ add/commit → push まで行う。`--no-commit` / `--no-push` で段階を止められる。

## commitメッセージ

- 日次・トピック: `log: YYYY-MM-DD <summary>`
- タスク: `task: <id> <summary>`（[tasks.md](tasks.md)）
- ハンドオフ: `handoff: YYYY-MM-DD <summary>`（[handoff.md](handoff.md)）

## 手動で commit / push する場合

```bash
git -C ~/ai-log-data add -- "daily/$DATE/$AGENT.md"
git -C ~/ai-log-data commit -m "log: $DATE <summary>"
git -C ~/ai-log-data push
```

複数ファイルを触った場合も、**実際に書いたパスだけ**を `git add` する。

## 失敗時

- pull / rebase が失敗したら、勝手に resolve せず原因を報告する
- push が失敗したら local commit は残し、原因を報告する
- dirty な無関係ファイルがあっても `git add -A` で巻き込まない
