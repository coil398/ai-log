---
name: ai-log
description: 時系列の作業ログ・進捗・ハンドオフをai-log-dataへ書く。セッション終了や担当交代の引き継ぎ、今日やったことのchronological記録で使う。横断再利用の学びはai-ltm、感想はai-diaryへ置き、同じ内容を二重保存しない。
---

# AI Work Log

`~/ai-log-data/` を使い、AIエージェントの時系列作業ログとハンドオフを Markdown で保存・同期する。

長期記憶（横断検索向けの学び・失敗・意思決定）は ai-ltm。感想は ai-diary。本スキルは「いつ・何をしたか」と「次の担当への引き継ぎ」だけを扱う。

## 発動とrouting

| 場面 | 行動 |
|---|---|
| 意味のある作業区切り・セッション終了・長い離席 | [record-and-sync.md](references/record-and-sync.md) の日次ログ追記 |
| 別エージェント／別セッションへの引き継ぎ | [handoff.md](references/handoff.md) |
| データディレクトリがない・初回 | `git clone` で `~/ai-log-data` を用意（公開READMEのセットアップ） |
| レイアウト・ファイル命名の確認 | [layout.md](references/layout.md) |

再利用価値のある学び・失敗・意思決定・中断点は ai-ltm へ。感想・日記は ai-diary へ。同じ内容を二重保存しない。

このSkillの実体directoryを `SKILL_DIR` とし、scriptはそこから絶対pathで解決する。タイムゾーンは Asia/Tokyo（JST）。

## 記録内容

日次ログに書くのは次のいずれか。見出しは `## HH:MM JST <title>`。本文は簡潔に。

- 実施した作業と結果
- いまの状態・ブロッカー・次のstep
- 触ったリポジトリ・PR・issue（公開可能な識別子のみ）
- ハンドオフに必要なコンテキスト（秘密情報を除く）

password・token・secret key・個人を特定できる社内情報は書かない。例外の扱いはプライベートなデータリポジトリ README のみ。

## 同期の原則

記録の直前に該当referenceだけを読む。手順は常に次の順。

1. `git -C ~/ai-log-data pull --rebase`
2. 対象ファイルだけを作成・追記
3. 触ったファイルだけ `git add`（`git add -A` 禁止）
4. commit: `log: YYYY-MM-DD <summary>` / ハンドオフは `handoff: YYYY-MM-DD <summary>`
5. `git push`

補助script:

```bash
python3 "$SKILL_DIR/scripts/new_entry.py" \
  --repo ~/ai-log-data \
  --agent <agent-name> \
  --title "<title>" \
  --body "<body>"
```
