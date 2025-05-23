# python-peojects
## explore python projects,instereing program
### please access .venv\Scripts\activate activate venv environment
## first projects
### cd file-sharing 
### run python file-sharing.py you can see the qrcode or python file-sharing.py --dir <目录路径> --port <端口号> 
### sumarize the projects
#### 启动一个 HTTP 服务器，共享指定目录下的文件
#### 生成二维码，指向服务器地址
#### 自动打开浏览器展示二维码和链接
#### 程序退出时清理临时文件（index.html 和 myqr.png）
#### 支持命令行参数设置端口和共享目录


##### 1. 解析命令行参数 (--dir, --port)
##### 2. 获取用户桌面路径（默认目录）
##### 3. 切换当前工作目录到目标目录
##### 4. 获取本机局域网 IP 地址
##### 5. 检查指定端口是否被占用
##### 6. 生成二维码文件 (myqr.png)
##### 7. 生成 index.html 页面（包含二维码和链接）
##### 8. 启动 HTTP 服务器，监听指定 IP 和端口
##### 9. 程序退出时清理临时文件
