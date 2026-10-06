# タスク（pickup / handback）

継続する仕事・定例・未完了を、どのボットでも拾える単位で持つ。  
データ側の実体は `~/ai-log-data/tasks/`。

日次ログ（[record-and-sync.md](record-and-sync.md)）は「今日何をしたか」。  
ハンドオフ（[handoff.md](handoff.md)）は薄いポインタでもよい。**作業状態の正本はタスクファイル。**

## 担当の分け方（最終・ai-log-data）

- **仕事 → Hermes**（`host: hermes`, `bot: main`, `owner: hermes-main`）  
  AlphaInsiders・Astran・コード／スクリプト・work-log。
- **日常生活 → Grok Bot**（`host: grokbot` + 係 `bot`）  
  通勤（`yajiuma`）、ゆりかもめ（`shirabe`）、健康・私生活。

### 棚卸し（inventory）

各ボットは定期的に `tasks/INDEX.md` と自分のタスクを読む。`status` と「次にやること」を更新し、新規に引き受けた仕事はタスク追加、古いものはフラグする。

```bash
git -C ~/ai-log-data add -- tasks/INDEX.md tasks/<id>.md
git -C ~/ai-log-data commit -m "task(<host>): inventory <bot> YYYY-MM-DD"
git -C ~/ai-log-data push
```

## ソース接頭辞

`host` と `bot` を front matter に書き、`owner` / `updated_by` / `履歴` は **`<host>-<bot>`**（例: `hermes-main`, `grokbot-sosui`, `grokbot-keizai`）。未割当は `unassigned`。  
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
host: hermes     # hermes = 仕事 / grokbot = 生活
bot: main        # hermes-main → bot: main。生活側は yajiuma / shirabe 等
owner: hermes-main   # 必ず <host>-<bot>（または unassigned）
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
   - `host` / `bot` / `owner`（=`<host>-<bot>`）/ `updated_by` を自分に合わせる
   - `updated` を今日（Asia/Tokyo）に
   - `履歴` に pickup 行を追記
4. INDEX の host / bot / owner 列も合わせる

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
