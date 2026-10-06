# ハンドオフ

別セッション・別ホスト／ボットへ作業を渡すときだけ読む。

## いつ書くか

- 担当ホスト／ボットが交代する
- 長い離席の前に、再開条件を残す必要がある
- 日次ログだけでは次の担当が再開できない

単なる進捗メモは日次ログ（[record-and-sync.md](record-and-sync.md)）へ。**継続する仕事の状態は [tasks.md](tasks.md)（`tasks/<id>.md`）へ。** 横断で再利用する学びは ai-ltm へ。ハンドオフファイルは薄いポインタでよい。

## ファイル

```
~/ai-log-data/handoffs/YYYY-MM-DD-<from-host>-to-<to-host>.md
```

例: `2026-10-06-grokbot-to-hermes.md`。詳細ディレクトリを置く場合も同じ stem にする。

## 推奨構成

```markdown
---
date: YYYY-MM-DD
type: handoff
from: <host>-<bot>
to: <host>-<bot-or-anyone>
from_host: <host>
to_host: <host>
status: open
---

# <短いタイトル>

## 現状

（いま動いているもの・止まった地点。詳細は tasks へのリンク）

## 渡したタスク

- [ ] tasks/<id>.md …

## ブロッカー / 注意

- （秘密情報は書かない）

## 参照

- 関連PR・issue・パス
```

## 同期

```bash
git -C ~/ai-log-data pull --rebase
git -C ~/ai-log-data add -- "handoffs/YYYY-MM-DD-<from-host>-to-<to-host>.md"
git -C ~/ai-log-data commit -m "handoff(<from-host>): YYYY-MM-DD to <to-host>"
git -C ~/ai-log-data push
```

日次ログにも「ハンドオフを書いた」旨を一行残してよいが、本文の重複は避ける。渡すタスクの `owner` も更新する。
