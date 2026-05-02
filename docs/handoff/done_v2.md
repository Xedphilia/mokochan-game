# タスク: mokochan-game JavaScript の「できた」画面実装

## 入力
`/tmp/claude/mokochan_script_masked.js` に元のスクリプト全文がある(base64画像はプレースホルダー `data:image/jpeg;base64,IMG` に置換済み)。

## 出力
編集後の完全なJavaScriptを `/tmp/claude/mokochan_script_edited.js` に書き出す。

## 編集要件

### 1. `openScreen` 関数の `tab==="done"` 分岐を置き換える
現状:
```js
else if(tab==="done")screenCard.innerHTML=`<h2>できた</h2><p>チェックリストは次版で再接続します。</p>`;
```
これを以下に置き換える(関数呼び出しに):
```js
else if(tab==="done")renderDoneScreen();
```

### 2. 新規関数 `renderDoneScreen` を追加
`tasks` 配列を使って10件のタスクカードを描画する:
- 上部: `<h2>できた</h2>` + 進捗表示 `<p>${completed.size}/${tasks.length} 完了 ・★+${totalPoints}pt</p>`
- 各タスクカード(縦リスト・gap 10px・padding 16px・max-height 70vh で overflow-y auto):
  - 絵文字(font-size: 28px)
  - ラベル(flex 1, font-size 16px, font-weight 600)
  - 「できた」ボタン または "✓ 完了" バッジ
- 完了済カード: `background:#e8f5e9; opacity:.85`
- 未完了ボタン: `background:#f47d83; color:#fff; border:0; border-radius:12px; padding:8px 16px; font-weight:700; cursor:pointer`
  - onclick で `markTaskDone('breakfast')` 呼び出し
- 完了バッジ(disabled): `background:#c5e1a5; color:#33691e; border-radius:12px; padding:8px 16px; font-weight:700`
- 全件完了したら最下部に `<p style="text-align:center;margin-top:16px;color:#33691e;font-weight:700">今日もお疲れさま!</p>` を追加

### 3. 新規関数 `markTaskDone(taskId)` を追加
- `completed.has(taskId)` なら何もしない(二重押し防止)
- `completed.add(taskId)`
- `totalPoints += 10`
- `updateStatus()` 呼び出し
- `saveState()` 呼び出し
- `renderDoneScreen()` で再描画

### 4. 新規関数 `saveState()` を追加
```js
function saveState(){
  try{
    const today=new Date().toISOString().slice(0,10);
    localStorage.setItem('mokochan_state_v1',JSON.stringify({completed:[...completed],totalPoints,hunger,savedDate:today}));
  }catch(e){}
}
```

### 5. 新規関数 `loadState()` を追加
```js
function loadState(){
  try{
    const raw=localStorage.getItem('mokochan_state_v1');
    if(!raw)return;
    const s=JSON.parse(raw);
    const today=new Date().toISOString().slice(0,10);
    totalPoints=s.totalPoints||0;
    hunger=s.hunger||100;
    if(s.savedDate===today){
      completed=new Set(s.completed||[]);
    }else{
      completed=new Set();
    }
  }catch(e){}
}
```

### 6. window load の `updateStatus()` 直前に `loadState()` を追加
現状:
```js
window.addEventListener("load",()=>{updateStatus();playLoopState("idle");setTimeout(()=>chooseRandomLivingState(),800);});
```
を以下に変更:
```js
window.addEventListener("load",()=>{loadState();updateStatus();playLoopState("idle");setTimeout(()=>chooseRandomLivingState(),800);});
```

### 7. hunger 自動減少の setInterval にも saveState を追加
現状:
```js
setInterval(()=>{if(hunger>1){hunger--;updateStatus();}},180000);
```
を以下に:
```js
setInterval(()=>{if(hunger>1){hunger--;updateStatus();saveState();}},180000);
```

## 制約
- base64画像のプレースホルダー `data:image/jpeg;base64,IMG` は**絶対に触らない**(個数も増減させない)
- 既存の関数 (stopAllVideos, playLoopState, showLoadingThen 等) は一切変更しない
- 新規関数の追加位置は openScreen 関数の直後が適切
- インデント・フォーマットは元のmin形式に従う(各関数1行でも良い・コンパクトに)
- 改行は最小限、minified 形式を維持
- 出力ファイル: `/tmp/claude/mokochan_script_edited.js`

## 検証
出力後、以下を確認:
1. `data:image/jpeg;base64,IMG` の出現回数が元の `mokochan_script_masked.js` と一致すること(grep -c で同数)
2. `renderDoneScreen`, `markTaskDone`, `saveState`, `loadState` が定義されていること
3. `openScreen` 関数の `tab==="done"` 分岐が `renderDoneScreen()` を呼んでいること
4. `loadState()` が window.load ハンドラ内で呼ばれていること
