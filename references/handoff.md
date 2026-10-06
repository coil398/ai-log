# ハンドオフ

別セッション・別エージェントへ作業を渡すときだけ読む。

## いつ書くか

- 担当エージェントが交代する
- 長い離席の前に、再開条件を残す必要がある
- 日次ログだけでは次の担当が再開できない

単なる進捗メモは日次ログ（[record-and-sync.md](record-and-sync.md)）へ。**継続する仕事の状態は [tasks.md](tasks.md)（`tasks/<id>.md`）へ。** 横断で再利用する学びは ai-ltm へ。ハンドオフファイルは薄いポインタでよい。

## ファイル

```
~/ai-log-data/handoffs/YYYY-MM-DD-<slug>.md
```

`<slug>` は短い英語またはローマ字（例: `hermes-handoff`, `release-cutover`）。

## 推奨構成

```markdown
---
date: YYYY-MM-DD
type: handoff
from: <agent-or-session>
to: <agent-or-session-or-anyone>
status: open
---

# <短いタイトル>

## 現状

（いま動いているもの・止まった地点）

## やったこと

- …

## 次にやること

- [ ] …

## ブロッカー / 注意

- （秘密情報は書かない）

## 参照

- 関連PR・issue・パス（公開可能なもの）
```

## 同期

```bash
git -C ~/ai-log-data pull --rebase
# handoffs/YYYY-MM-DD-<slug>.md を作成
git -C ~/ai-log-data add -- "handoffs/YYYY-MM-DD-<slug>.md"
git -C ~/ai-log-data commit -m "handoff: YYYY-MM-DD <summary>"
git -C ~/ai-log-data push
```

日次ログにも「ハンドオフを書いた」旨を一行残してよいが、本文の重複は避ける。
