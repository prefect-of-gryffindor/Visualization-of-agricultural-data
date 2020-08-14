from flask import Flask
from flask import render_template  # 渲染

app = Flask(__name__)


@app.route('/')  # 主页地址,“装饰器”
def news():
    return 'hello word'

if __name__ == '__main__':
    app.run()  # 127.0.0.1 回路 自己返回自己