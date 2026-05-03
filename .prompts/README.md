# .prompts/ - 画像生成プロンプト保存

Gemini 2.5 Flash Image または ComfyUI+FLUX で生成した画像のプロンプトを保存する。
npaka123「Codexゲーム開発プロンプトまとめ」のワークフローに基づく。

同じアセットを再生成・バリエーション作成するときにここから参照する。

## ファイル命名規則
`<アセット名>.md`

例:
- `food_icons.md`
- `gacha_banner.md`

## テンプレート
```markdown
# [アセット名]

## 生成日
YYYY-MM-DD

## ツール
Gemini 2.5 Flash Image / ComfyUI FLUX.1-schnell

## プロンプト（英語）
cute round bear, [description], transparent background, 
pixel art style, 64x64, white outline

## ネガティブプロンプト（ComfyUIの場合）
realistic, 3d, dark, scary

## 生成設定
- サイズ: 64x64 / 256x256 / etc
- Steps: 20
- CFG: 7

## 生成済みファイル
- assets/food_apple.png
- assets/food_ramen.png

## 使用箇所
- food タブのご飯リスト
```
