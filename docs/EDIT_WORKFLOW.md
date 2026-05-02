# index.html 編集ワークフロー

最終更新: 2026-05-01

## 前提

`index.html` は **3.3MB の minified HTML**。base64 画像が12個埋め込まれている。
1MB超のため codex に直接渡すと出力サイズ制限で編集が適用されない。
以下の固定パイプラインで処理する。

## パイプライン (8ステップ)

```
[index.html (3.3MB)]
    ↓ Step 1: <script>抽出
[mokochan_script.js (~984KB)]
    ↓ Step 2: base64画像をプレースホルダー化
[mokochan_script_masked.js (~5KB)] ← codex に渡せるサイズ
    ↓ Step 3: HANDOFF.md 作成
    ↓ Step 4: codex deep 委譲
[mokochan_script_edited.js]
    ↓ Step 5: プレースホルダー数の整合性確認
    ↓ Step 6: base64 を順次復元
[mokochan_script_restored.js (~986KB)]
    ↓ Step 7: 検証チェーン (node --check, クリック動作確認)
    ↓ Step 8: index.html に反映
[index.html (新版)]
```

## 詳細手順

### Step 1: <script> 抽出

```bash
python3 -c "
import re
with open('/Users/xedphilia_/claude_setup/mokochan-game/index.html') as f:
    html = f.read()
m = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
with open('/tmp/claude/mokochan_script.js', 'w') as f:
    f.write(m.group(1))
"
```

### Step 2: base64 マスク

```bash
python3 -c "
import re
with open('/tmp/claude/mokochan_script.js') as f:
    js = f.read()
masked = re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', 'data:image/jpeg;base64,IMG', js)
with open('/tmp/claude/mokochan_script_masked.js', 'w') as f:
    f.write(masked)
print('IMG count:', masked.count('IMG'))
"
```

### Step 3: HANDOFF.md 作成

`docs/handoff/<feature>_v<n>.md` に以下を記述:
- 入力ファイルパス (`mokochan_script_masked.js`)
- 出力ファイルパス (`mokochan_script_edited.js`)
- 編集要件 (関数追加・既存関数の置換等)
- 制約 (プレースホルダー個数を変えない・base64触らない・既存関数触らない)
- 検証項目

参考: `docs/handoff/done_v2.md`

### Step 4: codex deep 委譲

```bash
codex exec --skip-git-repo-check --profile deep "$(cat docs/handoff/<feature>_v<n>.md)"
```

`--skip-git-repo-check` は非gitディレクトリで必須。
codex deep は qwen3.6:35b-a3b、120 tok/s、SWE-Bench 50.3% 程度。

### Step 5: プレースホルダー数の整合性

```bash
diff <(grep -oc "data:image/jpeg;base64,IMG" /tmp/claude/mokochan_script_masked.js) \
     <(grep -oc "data:image/jpeg;base64,IMG" /tmp/claude/mokochan_script_edited.js)
```
出力が一致しなければ codex が画像を欠落 or 重複させた → 再委譲。

### Step 6: base64 復元

```bash
python3 -c "
import re
with open('/tmp/claude/mokochan_script.js') as f:
    original = f.read()
images = re.findall(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', original)
with open('/tmp/claude/mokochan_script_edited.js') as f:
    edited = f.read()
i = 0
def replace(m):
    global i
    img = images[i]
    i += 1
    return img
restored = re.sub(r'data:image/jpeg;base64,IMG', replace, edited)
with open('/tmp/claude/mokochan_script_restored.js', 'w') as f:
    f.write(restored)
print(f'Restored {i} images')
"
```

### Step 7: 検証チェーン (CRITICAL・順序厳守)

| # | 検証 | コマンド |
|---|---|---|
| 1 | 文法 | `node --check /tmp/claude/mokochan_script_restored.js` |
| 2 | 文字列連結エスケープ | `grep -E "\\\\'[+]\\w+[+]\\\\'" /tmp/claude/mokochan_script_restored.js` (空ヒットを期待) |
| 3 | スマートクォート/全角 | `python3 -c "f=open('/tmp/claude/mokochan_script_restored.js').read(); [print(c, f.count(c)) for c in '’“”（']"` |
| 4 | プレースホルダー数 | Step 5 と同等の確認 |
| 5 | 表示確認 | chrome-devtools MCP `take_screenshot` (URL `http://localhost:8768/index.html?v=N` を確認してから) |
| 6 | **クリック動作** | chrome-devtools MCP `click` で実ボタン押下 → 期待挙動を `evaluate_script` で検証 |

**Step 6 を絶対スキップしない**。文字列連結バグは文法だけ通って挙動が壊れる典型 (過去2回踏んだ)。

### Step 8: index.html に反映

```bash
python3 -c "
import re
with open('/Users/xedphilia_/claude_setup/mokochan-game/index.html') as f:
    html = f.read()
with open('/tmp/claude/mokochan_script_restored.js') as f:
    new_script = f.read()
new_html = re.sub(r'<script>.*?</script>', '<script>' + new_script + '</script>', html, count=1, flags=re.DOTALL)
with open('/Users/xedphilia_/claude_setup/mokochan-game/index.html', 'w') as f:
    f.write(new_html)
"
```

## 既知のハマりポイント

### codex deep の単一引用符エスケープバグ (2回踏んだ)
- 症状: `onclick="markTaskDone(\'+id+\')"` を生成
- JS の単一引用符内 `\'` は文字列を閉じないため `+id+` がリテラル文字列扱いに
- 修正: `\''+var+'\'` (close→concat→reopen) パターンに置換

```bash
python3 -c "
with open('/tmp/claude/mokochan_script_edited.js') as f: js = f.read()
fixed = js.replace(\"\\\\'+id+\\\\'\", \"\\\\''+id+'\\\\'\")
with open('/tmp/claude/mokochan_script_edited.js', 'w') as f: f.write(fixed)
"
```

### codex deep の壊れた文字列リテラル
- 症状: `'pt'+</p>';` のような不完全な式
- 修正: `node --check` のエラーメッセージから箇所特定 → Python regex で局所修正

### localStorage stale データ
- 症状: バグ修正後も古い不正データが残る
- 修正前にクリア:
```js
// chrome-devtools MCP の evaluate_script で実行
localStorage.removeItem('mokochan_state_v1')
```

## ローカル動作確認サーバー

```bash
cd ~/claude_setup/mokochan-game
python3 -m http.server 8768
```
URL: `http://localhost:8768/index.html?v=N` (N はバージョン)

`?v=N` のクエリは index.html のバージョン管理用 (キャッシュバスター兼用)
