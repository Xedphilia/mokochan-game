#!/usr/bin/env python3
"""
dev-server.py - index.html 変更を検知して接続中の全ブラウザを自動リロードするサーバー
index.html を永続変更せずにリロードスクリプトを動的注入します
ポート: 3000  /  使い方: python3 dev-server.py
"""
import http.server, socketserver, os, json, threading, time, socket

PORT = 3000
TARGET = "index.html"
_mtime = [0.0]

LIVERELOAD_SNIPPET = b"""<script>
(function(){var p=null;setInterval(function(){
  fetch('/_mtime').then(r=>r.json()).then(d=>{
    if(p===null){p=d.mtime;return;}
    if(d.mtime!==p){location.reload();}
  }).catch(function(){});
},1000);})();
</script>"""

def get_mtime():
    try: return os.path.getmtime(TARGET)
    except: return 0.0

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # mtime チェックエンドポイント
        if self.path == "/_mtime":
            data = json.dumps({"mtime": _mtime[0]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # index.html: リロードスクリプトを </body> 直前に動的注入
        if self.path in ("/", "/index.html"):
            try:
                with open(TARGET, "rb") as f:
                    content = f.read()
                content = content.replace(b"</body>", LIVERELOAD_SNIPPET + b"</body>", 1)
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self.send_error(500, str(e))
                return

        super().do_GET()

    def log_message(self, fmt, *args):
        msg = fmt % args if args else fmt
        if "/_mtime" not in msg:
            print(f"  {msg}")

def watch():
    while True:
        m = get_mtime()
        if m != _mtime[0]:
            _mtime[0] = m
        time.sleep(0.5)

if __name__ == "__main__":
    _mtime[0] = get_mtime()
    threading.Thread(target=watch, daemon=True).start()

    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "127.0.0.1"

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\n  ✅ Dev server 起動 (自動リロード有効)")
        print(f"  PC    : http://127.0.0.1:{PORT}/index.html")
        print(f"  スマホ  : http://{ip}:{PORT}/index.html")
        print(f"  ※ index.html を変更すると全端末が自動でリロードされます")
        print(f"  Ctrl+C で停止\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n停止しました")
