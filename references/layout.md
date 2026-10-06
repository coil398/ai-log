# データリポジトリのレイアウト

`~/ai-log-data`（プライベート）のディレクトリ規約。公開スキル側にはログ本文を置かない。

## ソース接頭辞

| 用途 | 形式 |
|---|---|
| 日次ファイル | `daily/YYYY-MM-DD/<host>-<bot>.md` |
| ハンドオフ | `handoffs/YYYY-MM-DD-<from-host>-to-<to-host>.md` |
| タスク actor | front matter に `host` / `bot`。owner / updated_by / 履歴は `<host>-<bot>` |
| commit | `<type>(<host>): <summary>`（type: log/task/handoff/docs/init） |

`host` 例: `grokbot`, `hermes`, `cursor`, `local-laptop`。`bot` 例: `sosui`, `main`。

## 全体図

```
ai-log-data/
  README.md
  .gitignore
  tasks/
    INDEX.md
    <id>.md
  context/
  handoffs/
    YYYY-MM-DD-<from-host>-to-<to-host>.md
    YYYY-MM-DD-<from-host>-to-<to-host>/   # 任意の詳細ディレクトリ
  daily/
    YYYY-MM-DD/
      <host>-<bot>.md
  topics/                      # 任意
```

## tasks/

- 継続する仕事の実行単位。書き方は [tasks.md](tasks.md)
- `INDEX.md` に status / owner 一覧を保つ

## context/

- 複数タスクが共有するルール・接続・ボット名簿

## daily/

- パス: `daily/YYYY-MM-DD/<host>-<bot>.md`
- front matter:

```markdown
---
date: YYYY-MM-DD
host: <host>
bot: <bot>
agent: <host>-<bot>
type: daily-work-log
---

## HH:MM JST <title>

（本文）
```

- 同一日・同一 `<host>-<bot>` への追記は末尾に `---` を挟んでから新しい `## HH:MM JST <title>` を足す
- 時刻は Asia/Tokyo（JST）

## handoffs/

- パス: `handoffs/YYYY-MM-DD-<from-host>-to-<to-host>.md`
- 厚い状態は tasks へ。書き方は [handoff.md](handoff.md)

## topics/（任意）

- `topics/<topic>/INDEX.md` ＋ `YYYY-MM-DD-<slug>.md`

## 置いてはいけないもの

- token・APIキー・本番資格情報
- 公開スキルリポジトリへのログ本文のミラー
