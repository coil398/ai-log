# AI Work Log (ai-log)

AIエージェント向けの**時系列作業ログ**システム。
セッション中に何をしたか・どこまで進んだか・次の担当への引き継ぎを Markdown で残し、プライベートなデータリポジトリへ同期する。

長期記憶（学び・失敗・意思決定の横断検索）は [ai-ltm](https://github.com/coil398/ai-ltm) の役割。感想・振り返りは [ai-diary](https://github.com/coil398/ai-diary)。本スキルは「いつ・何をしたか」のchronological logに特化する。

## 特徴

- 時系列ログ: 日付 × エージェント単位の日次ファイルに追記
- ハンドオフ: セッション間・エージェント間の引き継ぎを独立ファイルで残す
- トピック整理（任意）: テーマ別のINDEXと個別ノート
- Git同期: 触ったファイルだけをcommitし、プライベートリポジトリへpush
- 外部依存なし: shell / Python 標準機能と Git だけで動作

## 構成

```
ai-log/
├── SKILL.md                      # runtime 共通スキル定義
├── scripts/
│   └── new_entry.py              # 今日の日次ログを作成・追記し、触ったファイルだけcommit
└── references/
    ├── layout.md                 # データリポジトリのディレクトリ規約
    ├── record-and-sync.md        # 記録とgit同期手順
    └── handoff.md                # ハンドオフの書き方
```

## 必要環境

- Python 3
- Git
- タイムゾーン: Asia/Tokyo（ログ見出しの時刻は JST）

## セットアップ

スキルは `~/.agents/skills/ai-log/` などにインストールする想定。データは別リポジトリ `ai-log-data` をホームにクローンする。

```bash
# スキル（公開）
git clone https://github.com/coil398/ai-log.git ~/.agents/skills/ai-log

# データ（プライベート）
git clone git@github.com:coil398/ai-log-data.git ~/ai-log-data
# または HTTPS:
# git clone https://github.com/coil398/ai-log-data.git ~/ai-log-data
```

既存のリモートがある場合は `git clone <remote-url> ~/ai-log-data` でよい。

## 他スキルとのrouting

同じ内容を二重保存しない。行き先は次のとおり。

| 内容 | 行き先 |
|---|---|
| セッション横断で再利用する学び・失敗・意思決定・中断点 | [ai-ltm](https://github.com/coil398/ai-ltm) |
| 時系列の作業ログ・進捗・ハンドオフ | **ai-log**（本スキル） |
| 感想・振り返り・日記調の記録 | [ai-diary](https://github.com/coil398/ai-diary) |
| 今のcampaignだけの短期方針 | プロジェクト側の field-notes 等 |

## データレイアウト（要約）

詳細は [references/layout.md](references/layout.md)。

```
ai-log-data/
  README.md
  .gitignore
  handoffs/YYYY-MM-DD-<slug>.md
  daily/YYYY-MM-DD/<agent>.md
  topics/<topic>/INDEX.md + YYYY-MM-DD-<slug>.md   # 任意
```

日次ファイルは YAML front matter（`date` / `agent` / `type: daily-work-log`）を持ち、同一日内の追記は `---` で区切る。各セクション見出しは `## HH:MM JST <title>`。

## 同期ルール（要約）

詳細は [references/record-and-sync.md](references/record-and-sync.md)。

1. `git pull --rebase`
2. ファイルを書く / 追記する
3. **触ったファイルだけ** `git add`（`git add -A` は使わない）
4. commit: `log: YYYY-MM-DD <summary>`（ハンドオフは `handoff: YYYY-MM-DD <summary>`）
5. `git push`

秘密情報（token・本番パスワード・個人を特定できる社内情報など）は保存しない。例外の扱いはプライベートなデータリポジトリ側の README のみに記す。

## 使い方（日次ログの追加）

```bash
SKILL_DIR="$(cd ~/.agents/skills/ai-log && pwd -P)"
python3 "$SKILL_DIR/scripts/new_entry.py" \
  --repo ~/ai-log-data \
  --agent hermes \
  --title "作業の要約" \
  --body "やったこと・残件など"
```

`--no-commit` で書き込みだけ、`--message` でcommitメッセージの要約部分を上書きできる。
