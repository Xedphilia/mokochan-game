# HANDOFF: mokochan-game「できた」画面実装

## 対象ファイル
`/Users/xedphilia_/claude_setup/mokochan-game/index.html`

## 現状
`<script>` ブロック内の `openScreen` 関数で `tab==="done"` のとき:
```js
screenCard.innerHTML=`<h2>できた</h2><p>チェックリストは次版で再接続します。</p>`;
```
となっている。これを正式実装に置き換える。

`tasks` 配列(同スクリプト先頭)は定義済み:
```js
const tasks=[["breakfast","朝ごはん","☀️"],["lunch","昼ごはん","🌤️"],["dinner","夜ごはん","🌙"],["hands","手を洗う","🫧"],["cleanup","お片付け","🧸"],["change","お着替え","👕"],["teeth","歯みがき","🪥"],["bath","お風呂","🛁"],["toilet","トイレ","🚽"],["ready","お出かけ準備","🎒"]];
```

`completed` (Set), `totalPoints` (number), `updateStatus()`, `pointBadge`, `hungerValue` は宣言済み。

## 要件

### 1. 「できた」画面の DOM
`openScreen("done")` 時、`screenCard.innerHTML` に以下を組み立てる:

- ヘッダ: `<h2>できた</h2>` + 「今日のポイント: ★ Npt」表示
- 10件のタスクカード (縦リスト・grid 1列・gap 10px):
  - 各カード: 絵文字(大)・ラベル(中)・右端に「できた」ボタン (or 完了マーク)
  - 完了済タスクは: ボタンを"✓ 完了" にして disabled・カードを淡い緑背景にする
  - 未完了タスクの「できた」ボタンを押すと:
    - `completed.add(taskId)`
    - `totalPoints += 10`
    - `updateStatus()` を呼ぶ
    - localStorage に保存
    - 画面再描画 (openScreen("done") を再呼び出し)
- 全部完了したら下部に "今日もお疲れさま!" メッセージを表示

### 2. localStorage 永続化
- キー: `mokochan_state_v1`
- 保存内容: `{completed: [...completed], totalPoints, hunger, savedDate: "YYYY-MM-DD"}`
- 起動時(window load 直後)に読み込み:
  - `savedDate` が今日と一致 → completed/totalPoints/hunger を復元
  - 一致しない → completed をリセット (totalPoints/hungerは継続)
- 保存タイミング: タスク完了時・hunger変更時(既存setIntervalの中)

### 3. スタイル
既存の白カード・桃色アクセント(`#f47d83`)に統一:
- カード: `background: rgba(255,255,255,.96); border-radius: 14px; padding: 12px 14px; box-shadow: 0 2px 8px rgba(0,0,0,.08)`
- 完了カード: `background: #e8f5e9; opacity: .85`
- ボタン: `background: #f47d83; color: #fff; border: 0; border-radius: 12px; padding: 8px 16px; font-weight: 700`
- 完了ボタン(disabled): `background: #c5e1a5; color: #33691e`

### 4. レイアウト
画面カード本体は scroll 可能 (`max-height: 70vh; overflow-y: auto`) にして、10件全部見えるように。

## 実装方針
1. `openScreen` 関数の `tab==="done"` 分岐を書き換える
2. 別途 `renderDoneScreen()` ヘルパー関数を作って innerHTML 構築するとスッキリする
3. 完了ボタンの `onclick` は `markTaskDone('breakfast')` のような関数を呼ぶ形にする
4. `markTaskDone` / `loadState` / `saveState` を新規関数として追加
5. window load 時の `updateStatus()` 直後に `loadState()` を呼ぶ
6. localStorage 例外は try/catch で握りつぶす(localStorage無効環境でも壊れないように)

## 完了条件
- index.html を編集し、ブラウザで http://localhost:8768/index.html?v=7 をリロードして「できた」タブを開くと:
  - 10件のタスクカードが縦に並んでいる
  - 各カードに絵文字・ラベル・「できた」ボタンが見える
  - ボタン押下で完了状態に変わり、ヘッダのポイントが+10される
  - リロードしても完了状態が保持される

## 編集時の注意
- index.html は minified (1行に長く詰まっている)。`<script>` ブロックは比較的読める形なので、その中だけ編集する
- HTML body 内の他要素 (poster/video/nav 等) には触らない
- 既存の CSS・関数定義(`stopAllVideos`, `playLoopState` 等)は変更しない
- バージョン番号は HTML 最下部の `メニュー操作テスト v19` (CSS下) を v20 に上げる
