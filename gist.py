from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as p
import requests

def trim(path):
    path_que = p.urlparse(path).query
    q_par = p.parse_qs(path_que)
    URL_and_par = q_par['URL'][0]
    par = p.urlparse(URL_and_par).query
    URL = URL_and_par.replace('?' + par, '')
    par = p.parse_qs(par)
    par = par['param'][0]
    return par, URL

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')#これがないとリクエストに答えられない。js側エラー内容( No 'Access-Control-Allow-Origin' header is present on the requested resource.)
            self.end_headers()
            
            par, URL = trim(self.path)
            paramater = par
            result = None#念のため一度Noneで初期化
            
            res = requests.get(URL)#URLにGETする

            func_text = '''{}'''.format(res.text)#三連引用符を使うことで複数行の文を実行可能にする
            print(func_text)#Gist更新が遅い時があるのでどんなコードを実行するか確認
            
            print()
            d = {}
            exec(func_text)#Gistのプログラムを実行、第3引数locals()でもdict型の変数でも大丈夫
            result = locals()['func'](paramater)
            # result = d['func'](paramater)#第3引数dict型変数の場合、()がとれて少しだけわかりやすい
            print(result)
            print()

            self.wfile.write(str(result).encode('utf-8'))#Scratchへの値渡し用

        except Exception as e:  
            print("An error occured")
            print("The information of error is as following")
            print(type(e))
            print(e.args)
            print(e)
            print()
            
def run(server_class=HTTPServer, handler_class=Server, server_name='', port=8000):

    server = server_class((server_name, port), handler_class)
    server.serve_forever()

print('start')
run(server_name='', port=8000)