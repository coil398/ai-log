# タスク（pickup / handback）

継続する仕事・定例・未完了を、どのボットでも拾える単位で持つ。  
データ側の実体は `~/ai-log-data/tasks/`。

日次ログ（[record-and-sync.md](record-and-sync.md)）は「今日何をしたか」。  
ハンドオフ（[handoff.md](handoff.md)）は薄いポインタでもよい。**作業状態の正本はタスクファイル。**

## ソース接頭辞

`owner` / `updated_by` / `履歴` の行為者は **`<host>-<bot>`**（例: `hermes-main`, `grokbot-sosui`）。未割当は `unassigned`。  
commit は `task(<host>): <id> <summary>`。

## ファイル

```
~/ai-log-data/tasks/INDEX.md
~/ai-log-data/tasks/<id>.md
~/ai-log-data/context/
```

`<id>` は短い英小文字・ハイフン（例: `fxnyao-weekly`）。

## Front matter

```yaml
---
id: fxnyao-weekly
title: fxnyao 週次解禁・収集
status: active   # active | paused | todo | done
owner: hermes-main
cadence: "Mon 07:30 JST"
updated: 2026-10-06
updated_by: grokbot-sosui
---
```

## 本文セクション（必須）

1. **目的**
2. **現状**
3. **次にやること**
4. **手順**
5. **判断基準**
6. **履歴** — 追記のみ。例: `- 2026-10-06: pickup by hermes-main`

## Pickup

1. `git -C ~/ai-log-data pull --rebase`
2. `tasks/INDEX.md` を確認。必要なら `context/` を読む
3. `tasks/<id>.md` を編集:
   - `owner` / `updated_by` を自分の `<host>-<bot>` に
   - `updated` を今日（Asia/Tokyo）に
   - `履歴` に pickup 行を追記
4. INDEX の owner 列も合わせる

```bash
git -C ~/ai-log-data add -- "tasks/<id>.md" "tasks/INDEX.md"
git -C ~/ai-log-data commit -m "task(<host>): <id> pickup"
git -C ~/ai-log-data push
```

## Handback / 完了

- 渡す: `owner` を次の `<host>-<bot>` または `unassigned`。`updated_by` を自分に。`履歴` に handback
- 完了: `status: done`
- commit: `task(<host>): <id> handback` / `task(<host>): <id> done` / `task(<host>): <id> <要約>`

## 新規タスク

1. `tasks/<id>.md` をテンプレで作成（`updated_by` 必須）
2. `tasks/INDEX.md` に1行追加
3. `task(<host>): <id> create` で commit
