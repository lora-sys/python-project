"-----coding:utf-8-----"
import os
import socket
import webbrowser
import pyqrcode
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import argparse
import atexit
PORT=8010
DIRECTORY_NAME='OneDrive'
QR_CODE_FILENAME='myqr.png'
INDEX_FILE = 'index.html'

# def parse_arg():
#     parser=argparse.ArgumentParser(description="Start a local http file sharing http server")
#     parser.add_argument("--dir--",default=get_desktop_path(),help="Directory to share")
#     parser.add_argument("--port--",type=int,default=PORT,help="Port number to use")
#     return parser.parse_args()
def get_desktop_path():
    
    home=os.path.expanduser('~')
    if os.name=='nt':
        return os.path.join(os.environ.get('USERPROFILE'),DIRECTORY_NAME)
    else:
        return os.path.join(home,DIRECTORY_NAME)
    
def get_local_adress():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # try:
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]
    # finally:
    #     return s.close()
    

def generate_qr_code(url,filename):
    qr=pyqrcode.create(url)
    if filename.endswith(".png"):
        qr.png(filename,scale=8)
    else:
        qr.svg(filename,scale=8)
    print("QR code generated")
    return filename
def is_port_use(port):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost',port)) == 0

def create_index_file(qr_file,link):
    content=f"""
    <html>
    <head><title>File sharing</title></head>
    <body style="font-family:sans-serif; text-align:center; padding:40px;">
    <h1>File Sharing service</h1>
    <p>please scan qrcode access link</p>
    <img src="{qr_file}" width="256" height="256"/>
    <p><a href="{link}">{link}</a></p>
    </body>
    </html>

    """
    with open(INDEX_FILE,"w",encoding='utf-8') as f:
        f.write(content)
    return INDEX_FILE
# class CustomHandler(SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.path=INDEX_FILE
#             return super().do_GET()
        

def clearup():
    if os.path.exists(QR_CODE_FILENAME):
        os.remove(QR_CODE_FILENAME)
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
def main():
    parser = argparse.ArgumentParser(description="启动一个本地 HTTP 文件共享服务器")
    parser.add_argument("--dir", default=get_desktop_path(), help="要共享的目录")
    parser.add_argument("--port", type=int, default=8010, help="使用的端口号")
    args = parser.parse_args()

    PORT = args.port
    target_dir = args.dir
    if is_port_use(PORT):
        print(f'端口 {PORT} 已被使用')
        return
    # covert work directory
    # 切换工作目录
    try:
        os.chdir(target_dir)
        print(f"当前工作目录: {os.getcwd()}")
    except FileNotFoundError:
        print(f"目录不存在: {target_dir}")
        return
    try:
        ip=get_local_adress()
    except Exception as e:
        print("Directory not found",e)
        return
    
    link=f"http://{ip}:{PORT}"

    qr_file=generate_qr_code(link,QR_CODE_FILENAME)
    try:
        webbrowser.open(qr_file)
    except Exception as e:
        print("Error opening browser",e)
    # create index.html 
    index_file=create_index_file(qr_file,link)
    atexit.register(clearup)
    #start server
    Handler=SimpleHTTPRequestHandler
    print(f"Current working directory: {os.getcwd()}")
    print(f"QR code file path: {os.path.abspath(QR_CODE_FILENAME)}")
    server_address=(ip,PORT)
    with TCPServer(server_address,Handler) as httpd:
        print(f"current port{PORT} provide server")
        print(f"link:{link}")
        print(f"qr code:{qr_file}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("server stoped")

if __name__=="__main__":
    main()