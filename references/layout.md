# データリポジトリのレイアウト

`~/ai-log-data`（プライベート）のディレクトリ規約。公開スキル側にはログ本文を置かない。

## 全体図

```
ai-log-data/
  README.md
  .gitignore
  handoffs/
    YYYY-MM-DD-<slug>.md
  daily/
    YYYY-MM-DD/
      <agent>.md
  topics/                    # 任意
    <topic>/
      INDEX.md
      YYYY-MM-DD-<slug>.md
```

## daily/

- パス: `daily/YYYY-MM-DD/<agent>.md`
- `<agent>` はエージェント識別子（例: `hermes`, `claude`, `codex`）。小文字・ハイフン可
- 新規ファイルの front matter:

```markdown
---
date: YYYY-MM-DD
agent: <agent>
type: daily-work-log
---

## HH:MM JST <title>

（本文）
```

- 同一日・同一エージェントへの追記は、既存内容の末尾に `---` を挟んでから新しい `## HH:MM JST <title>` セクションを足す
- 時刻は Asia/Tokyo（JST）

## handoffs/

- パス: `handoffs/YYYY-MM-DD-<slug>.md`
- セッション間・エージェント間の引き継ぎ専用。日次ログの代替ではない
- 書き方は [handoff.md](handoff.md)

## topics/（任意）

- テーマ横断で拾いやすくしたいときだけ使う
- `topics/<topic>/INDEX.md` にリンク一覧
- 個別ノートは `YYYY-MM-DD-<slug>.md`（field-notes と同系統の命名）

## 置いてはいけないもの

- token・APIキー・本番資格情報
- 個人を特定できる社内名・プロジェクト秘密
- 公開スキルリポジトリへのログ本文のミラー
