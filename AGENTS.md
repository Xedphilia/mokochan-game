# モコちゃんゲーム - AGENTS.md
# Codex（ローカルLLM）への行動ルール

## ゲーム種別
タマゴッチ系ブラウザ育成ゲーム（単体HTML・GitHub Pages デプロイ）

## 技術スタック
- 単体ファイル: `index.html`（3.3MB・base64画像/動画埋め込み）
- localStorage キー: `mokochan_state_v1`（変更禁止）
- CSS animation + video 要素でアニメーション
- 外部ライブラリ: なし（依存ゼロを維持）

## 作業ルール
1. **PLAN.md を読んでから作業を開始する**
2. **完了後は `.logs/<機能名>_YYYY-MM-DD.md` に判断ログを残す**
3. **画像を生成した場合は `.prompts/<アセット名>.md` にプロンプトを保存する**
4. **1回の作業で変更するファイルは1つ（index.html のみ）**
5. **Playwright でブラウザ上の動作を確認してから完了報告する**

## 必須制約
- `localStorage` のキー名 `mokochan_state_v1` は変更禁止（ユーザーデータが消える）
- `food_data.js` と `collection_data.js` のデータ構造は変更しない（参照のみ）
- 外部CDNや外部ライブラリを追加しない（単体HTML維持）
- ファイルサイズが3MB超のため、大型編集はセクション抽出→マスク→編集→戻すパイプラインを使う

## 1MB超ファイル編集パイプライン
```
1. 対象セクション（<script>ブロック）を /tmp/claude/<name>_section.js に抽出
2. base64データをプレースホルダーに置換 → /tmp/claude/<name>_masked.js（5KB前後）
3. codex deep で編集 → /tmp/claude/<name>_edited.js
4. プレースホルダー数の整合性確認
5. 元データ復元 → /tmp/claude/<name>_restored.js
6. index.html に反映
```

## タブ別の実装状況
| タブ | 担当関数 | 状態 |
|---|---|---|
| room | playLoopState, playHappy, chooseRandomLivingState | 実装済み |
| done | renderDoneScreen, markTaskDone | 実装済み |
| food | openScreen('food') | **未実装** |
| gacha | openScreen('gacha') | プレースホルダー |
| collection | openScreen('collection') | プレースホルダー |
| menu | openScreen('menu') | プレースホルダー |

## 画像アセット生成（必要な場合）
- **UIアイコン・テキスト入り素材**: Gemini 2.5 Flash Image（GEMINI_API_KEY）
- **スプライト・背景・キャラクター**: ComfyUI + FLUX.1-schnell（ローカル無料）
- 生成後は必ず `.prompts/<名前>.md` にプロンプトを保存する
