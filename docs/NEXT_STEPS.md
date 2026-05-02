# 次のステップ (優先順位順)

最終更新: 2026-05-01

## 優先順位

| # | タブ | 優先度 | 概要 |
|---|---|---|---|
| 1 | food | 高 | 食事選択UI + hunger 回復ロジック |
| 2 | menu | 中 | 設定画面 (音量・通知ON/OFF・データリセット等) |
| 3 | gacha | 中 | ガチャアニメーション + コレクション連動 |
| 4 | collection | 低 | コレクション一覧の動的化 |

## 1. food タブ実装

### 現状
```js
else if(tab==="food")screenCard.innerHTML=`<h2>ご飯</h2><p>現在の満腹度：<b>${hunger}</b> / 100</p>`;
```

### 仕様案

**画面構成**:
- ヘッダ: `<h2>ご飯</h2>` + 満腹度バー (現在値/100, 視覚的なゲージ)
- 食事選択カード (3〜5件):
  - 絵文字 + 名前 + 回復量 + 「あげる」ボタン
- 全部食べた後の状態: 「もう満腹だよ」メッセージ

**食事リスト案** (`foods` 配列を tasks と同様に追加):
```js
const foods = [
  ["bread", "パン", "🍞", 10],
  ["rice", "ごはん", "🍚", 20],
  ["pasta", "パスタ", "🍝", 25],
  ["cake", "ケーキ", "🍰", 15],
  ["fruit", "フルーツ", "🍎", 8]
];
```

**ロジック**:
- ボタン押下 → `feedFood(id)` 呼び出し
- `hunger = Math.min(100, hunger + recoveryAmount)`
- `updateStatus()` + `saveState()`
- アニメーション (オプション): `playHappy()` を流用
- 満腹時 (`hunger >= 100`) はボタン disabled

**新規関数**:
- `renderFoodScreen()`
- `feedFood(foodId)`

### 実装手順
1. `docs/EDIT_WORKFLOW.md` のパイプラインに従う
2. HANDOFF を `docs/handoff/food_v1.md` として作成
3. codex deep に委譲
4. 検証チェーン6ステップ実施
5. PROJECT_STATE.md と本ファイルを更新

## 2. menu タブ実装

### 現状
プレースホルダー `<h2>メニュー</h2><p>設定画面です</p>` のみ

### 仕様案

| 項目 | 内容 |
|---|---|
| 音量設定 | スライダー (BGM/SE別) |
| 通知ON/OFF | トグル |
| データリセット | localStorage クリアボタン (確認モーダル付き) |
| バージョン情報 | 現在のバージョン表示 |
| 利用規約・クレジット | リンクまたはモーダル |

## 3. gacha タブ動的化

### 現状
ガチャ.png の静的表示のみ

### 仕様案

- ガチャ実行ボタン
- ポイント消費 (例: 10pt = 1回)
- アイテム抽選アニメーション (CSS or 動画)
- 排出結果を collection に追加 (新規キー `mokochan_collection_v1`)
- レアリティ別の演出

## 4. collection タブ充実

### 現状
画像2枚のハードコード

### 仕様案

- ガチャ獲得アイテムのグリッド表示
- 未取得は影で表示 (シルエット)
- 獲得済みのタップで詳細モーダル
- ストレージ: `localStorage` キー `mokochan_collection_v1`

## 共通注意事項

- 新規タブ実装は必ず `docs/EDIT_WORKFLOW.md` のパイプライン経由
- localStorage キーはバージョン suffix を付ける (将来のスキーマ変更対応)
- 既存 `mokochan_state_v1` のスキーマ拡張時は loadState() の互換処理を入れる
- 動画埋め込みは base64 で index.html 内・サイズ膨張に注意
