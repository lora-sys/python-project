import os
import socket
import webbrowser
import pyqrcode
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

PORT=8010
DIRECTORY_NAME='OneDrive'
QR_CODE_FILENAME='myqr.svg'

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
    qr.svg(filename,scale=8)
    print("QR code generated")
    return filename

def main():
    target_dir=get_desktop_path()
    try:
        os.chdir(target_dir)
        print("Current working directory:",os.getcwd())
    except FileNotFoundError:
        print("Directory not found")
        return
    
    ip=get_local_adress()
    link=f"http://{ip}:{PORT}"

    qr_file=generate_qr_code(link,QR_CODE_FILENAME)
    try:
        webbrowser.open(qr_file)
    except Exception as e:
        print("Error opening browser",e)
    
    Handler=SimpleHTTPRequestHandler
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