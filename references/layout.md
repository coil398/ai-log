# データリポジトリのレイアウト

`~/ai-log-data`（プライベート）のディレクトリ規約。公開スキル側にはログ本文を置かない。

## 全体図

```
ai-log-data/
  README.md
  .gitignore
  tasks/
    INDEX.md
    <id>.md
  context/                     # 共有文脈（任意）
    …
  handoffs/
    YYYY-MM-DD-<slug>.md
  daily/
    YYYY-MM-DD/
      <agent>.md
  topics/                      # 任意
    <topic>/
      INDEX.md
      YYYY-MM-DD-<slug>.md
```

## tasks/

- 継続する仕事・定例・未完了の**実行単位**
- 書き方・pickup/handback は [tasks.md](tasks.md)
- `INDEX.md` に全タスクの status / owner 一覧を保つ

## context/

- 複数タスクが共有するルール・接続・ボット名簿など
- タスク本体の代替ではない

## daily/

- パス: `daily/YYYY-MM-DD/<agent>.md`
- `<agent>` はエージェント識別子（例: `hermes`, `grok-bot`）。小文字・ハイフン可
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
- セッション間・エージェント間の薄い引き継ぎ。厚い状態は tasks へ
- 書き方は [handoff.md](handoff.md)

## topics/（任意）

- テーマ横断で拾いやすくしたいときだけ使う
- `topics/<topic>/INDEX.md` にリンク一覧
- 個別ノートは `YYYY-MM-DD-<slug>.md`

## 置いてはいけないもの

- token・APIキー・本番資格情報
- 個人を特定できる社内名・プロジェクト秘密（ユーザーが明示した例外を除く）
- 公開スキルリポジトリへのログ本文のミラー
