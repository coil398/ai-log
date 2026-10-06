# タスク（pickup / handback）

継続する仕事・定例・未完了を、どのボットでも拾える単位で持つ。  
データ側の実体は `~/ai-log-data/tasks/`。

日次ログ（[record-and-sync.md](record-and-sync.md)）は「今日何をしたか」。  
ハンドオフ（[handoff.md](handoff.md)）は薄いポインタでもよい。**作業状態の正本はタスクファイル。**

## ファイル

```
~/ai-log-data/tasks/INDEX.md
~/ai-log-data/tasks/<id>.md
~/ai-log-data/context/          # 全タスク共通の文脈（任意で読む）
```

`<id>` は短い英小文字・ハイフン（例: `fxnyao-weekly`, `discord-bridge`）。

## Front matter

```yaml
---
id: fxnyao-weekly
title: fxnyao 週次解禁・収集
status: active   # active | paused | todo | done
owner: hermes    # hermes | grok-bot-総帥 | unassigned | …
cadence: "Mon 07:30 JST"   # または on-demand / event-driven
updated: 2026-10-06
---
```

## 本文セクション（必須）

1. **目的** — 何のための仕事か  
2. **現状** — いま動いているもの・止まった地点  
3. **次にやること** — チェックリスト可  
4. **手順** — 再現できる具体手順  
5. **判断基準** — 沈黙／報告／禁止事項  
6. **履歴** — **追記のみ**。日付付き（例: `- 2026-10-06: pickup by hermes`）

## Pickup

1. `git -C ~/ai-log-data pull --rebase`
2. `tasks/INDEX.md` で `status` / `owner` を確認。必要なら `context/` を読む
3. 対象 `tasks/<id>.md` を編集:
   - `owner` を自分の識別子に
   - `updated` を今日（Asia/Tokyo）に
   - `履歴` に pickup 行を追記
4. 触ったファイルだけ add（INDEX を触ったら INDEX も）

```bash
git -C ~/ai-log-data add -- "tasks/<id>.md" "tasks/INDEX.md"
git -C ~/ai-log-data commit -m "task: <id> pickup"
git -C ~/ai-log-data push
```

## 実行中

- `現状` / `次にやること` を更新する
- 意味のある区切りは日次ログにも一行（`log: …`）。同じ長文を二重保存しない

## Handback / 完了

- 渡す: `owner` を次の担当または `unassigned`。`履歴` に handback を追記
- 完了: `status: done`。必要なら INDEX も更新
- commit: `task: <id> handback` / `task: <id> done` / `task: <id> <短い要約>`

## 新規タスク

1. `tasks/<id>.md` を上記テンプレで作成  
2. `tasks/INDEX.md` の表に1行追加  
3. `task: <id> create` で commit  

共有ルール・接続情報はタスクに埋め込まず `context/` へ。
