# mokochan-game プロジェクト現状

最終更新: 2026-05-01

## 概要
- 単体HTML型のWebアプリ試作版
- ファイル: `index.html` (3.3MB minified・base64画像/動画埋め込み)
- バックアップ: `index.html.bak` (2.8MB・前世代版)
- GitHub Pages デプロイ前提

## バージョン履歴

| ver | 内容 | 日付 |
|---|---|---|
| v19 | README記載の試作版 (ベース) | 〜2026-04 |
| v6 | ナビゲーション微調整 (アイコン拡大・メニュー/コレクション位置入替・最右パディング・コレクションアイコン透過処理) | 2026-05-01 |
| v7 | 「できた」画面のタスクチェックリスト初版 (codex deep 委譲) | 2026-05-01 |
| v8 | v7 の文字列連結バグ修正版・本番反映 | 2026-05-01 |

**注意**: HTML本文末尾の表示文字列は今でも「メニュー操作テスト v19」のまま。バージョン番号はソース内では更新せずURLクエリ `?v=8` で識別している。

## タブ構造 (画面)

`openScreen(tab)` 関数の分岐先:

| tab | 状態 | 説明 |
|---|---|---|
| `room` | 既存 | リビング背景動画+状態切替 (idle/おもちゃ遊び/椅子遊び) |
| `done` | **v8で実装** | 10件タスクのチェックリスト+ポイント加算 |
| `food` | **未実装** | hunger表示のみ。ご飯選択+回復ロジック未実装 |
| `gacha` | プレースホルダー | ガチャ.png 静的表示のみ |
| `collection` | プレースホルダー | 画像2枚のみ |
| `menu` | プレースホルダー | "設定画面です" のみ |
| `talk` | 既存 | (詳細未調査) |

## 関数マップ

| 関数 | 役割 |
|---|---|
| `openScreen(tab)` | タブ切替・各画面の innerHTML 構築 |
| `renderDoneScreen()` | 「できた」画面描画 (v8新規) |
| `markTaskDone(taskId)` | タスク完了処理・ポイント加算・保存 (v8新規) |
| `saveState()` | localStorage 永続化 (v8新規) |
| `loadState()` | localStorage 復元・日付チェック (v8新規) |
| `updateStatus()` | ヘッダのポイント・hunger 表示更新 |
| `playLoopState(state)` | 動画ループ再生 (idle等) |
| `playHappy()` | ハッピーモーション再生 |
| `chooseRandomLivingState()` | リビングのランダム状態選択 |
| `returnToIdleWithLoading()` | idle 状態への復帰 |
| `stopAllVideos()` | 全動画停止 |
| `showLoadingThen(callback)` | ローディング表示+コールバック |
| `setActive(el)` | ナビのアクティブ状態切替 |
| `sleep(ms)` | 待機 (Promise) |

## 状態変数 (グローバル)

| 変数 | 型 | 役割 |
|---|---|---|
| `tasks` | `Array<[id, label, emoji]>` | 10件のタスク定義 (定数) |
| `completed` | `Set<string>` | 完了済タスクのID集合 |
| `totalPoints` | `number` | 累積ポイント |
| `hunger` | `number` | 満腹度 (0-100, 3分毎に -1) |
| `busy` | `boolean` | 動画切替中フラグ |

### tasks 配列の中身

```js
const tasks = [
  ["breakfast","朝ごはん","☀️"],
  ["lunch","昼ごはん","🌤️"],
  ["dinner","夜ごはん","🌙"],
  ["hands","手を洗う","🫧"],
  ["cleanup","お片付け","🧸"],
  ["change","お着替え","👕"],
  ["teeth","歯みがき","🪥"],
  ["bath","お風呂","🛁"],
  ["toilet","トイレ","🚽"],
  ["ready","お出かけ準備","🎒"]
];
```

## 永続化

| 項目 | 内容 |
|---|---|
| ストレージ | localStorage |
| キー | `mokochan_state_v1` |
| 保存内容 | `{completed: [...], totalPoints, hunger, savedDate: "YYYY-MM-DD"}` |
| 日付不一致時 | `completed` をリセット (`totalPoints`/`hunger` は継続) |
| 保存タイミング | タスク完了時・hunger 自動減少時 |

## 既知の制約

- `index.html` は3.3MB (base64画像12個含む) のため、編集時は `docs/EDIT_WORKFLOW.md` のパイプライン必須
- ソース末尾の表示バージョン文字列はv19のまま (URL `?v=N` で実バージョン管理)
- GitHub Pages 想定だがリポジトリ未作成
