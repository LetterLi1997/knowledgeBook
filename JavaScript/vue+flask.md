# vue+nginx+gunicorn+flask 部署到生产环境
## 先说结论
1. 部署到生产环境前首先是要保证本地部署vue(production)+nginx+gunicorn(用于开启多线程flask提高性能)
2. linux真是优秀的系统(但是一定要注意安装、卸载东西要谨慎。因为可能导致配置文件啥的出错，会浪费较多时间)
3. 前后端分离的项目新手阶段尽量要避免跨域。

## 说说框架选择
### 关于Vue
用的是vue框架 + element-admin模板，是一个很好的前后端分离学习模板。

通过它的api向后端发起请求，同时模板中自带了mock用于初步的接口调试。mock可以帮助只会前端的程序员实现接口测试、数据模拟的效果。

### 关于flask
最初选择flask是因为python是一门熟悉的语言，而且flask也是轻量级框架，支持很多种拓展，想选啥数据库引擎就选啥，用mongoDB、mysql啥的都行。

### 关于nginx
nginx已经流行了有10年左右的历史，都称赞nginx是一种高性能的反向代理、负载均衡服务器。并且可以用来直接请求静态页面，让后端专注于响应请求。所以这里面用来做前后端的纽带也正常不过。

## 开始部署 - 保证本地可以运行
### 1.本地-前端部分
- 以vue-element-admin这个模板为例。base_api:改为服务器中想要访问的ip及路径

```BASE_API:'"url/api/"'```

这里需要注意的是： 尽量不要写成
```
BASE_API:'"url:port/api"'
比如 BASE_API:'"url:8081/api"'
```
这样带来的问题就是前端跨域，具体的处理操作我也不清楚...
- 更改prod.env.js中的assetsPublicPath从"/"改为"./"
- 在webpack.prod.conf.js 找到 output:{} 其中增加 pulicPath: './'
- 接下来就是打包 ```npm run dev```

将打包后的dist文件夹放入flask项目根目录下
### 2.本地-后端部分
因为flask本身开启服务占用了一个端口，同时对外提供api也要占用一个端口。这其实已经构成了跨域，通过python-cors这个模块使app能够解决跨域问题。
1. flask app入口
```
from app import create_app
from flask_sqlalchemy import SQLAlchemy

app = create_app()

if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()

```
2. 创建flask实例

就是如下的CORS相关代码
```
"""
author: LetterLi
time:2019/4/7 14:04

"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
db = SQLAlchemy()
migrate = Migrate()

# blueprint from 一定是写到相应文件名为止的 然后再 imprt 方法名
from app.api import bp
from app.config import Config
# Flask-SQLAlchemy plugin SQLAlchemy是一个类，db相当于实例化一个对象

def create_app(config_class=Config):
    app = Flask(__name__,static_folder="../dist/static",template_folder='../dist')
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}}, methods=['GET', 'HEAD', 'POST', 'OPTIONS'])
    # Init Flask-SQLAlchemy
    db.init_app(app)
    migrate.init_app(app,db)

    from app.api import userlist
    with app.app_context():
        db.create_all()
    # register blueprint
    app.register_blueprint(bp)

    # @app.route('/')
    # def index():
    #     return render_template("index.html")

    return app

```
3. 本地-nginx部分

已经加入了跨域处理请求头的部分，并且加入if判断，如果是option初始请求头无须返回，可以略微加快响应速度。
```
user nginx;
worker_processes auto;
pid /run/nginx.pid;

events {
	worker_connections 768;
	# multi_accept on;
}

http {

	##
	# Basic Settings
	##

	sendfile on;
	tcp_nopush on;
	tcp_nodelay on;
	keepalive_timeout 65;
	types_hash_max_size 2048;
	# server_tokens off;

	# server_names_hash_bucket_size 64;
	# server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	##
	# SSL Settings
	##

	ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;

	##
	# Logging Settings
	##

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	##
	# Gzip Settings
	##

	gzip on;
	gzip_disable "msie6";

	# gzip_vary on;
	# gzip_proxied any;
	# gzip_comp_level 6;
	# gzip_b上述uffers 16 8k;
	# gzip_h上述ttp_version 1.1;
	# gzip_t上述ypes text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

	##
	# Virtual Host Configs
	##
	server {
            listen          80;
            server_name     ee.zju.edu.cn;

            location /thxt {
		add_header Access-Control-Allow-Origin *;
	        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
    	  	add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';

	        if ($request_method = 'OPTIONS') {
		    上述return 204;
	        }

                alias /home/letterli/IT/Vue/ee-talk-backend/dist/;
                # try_files $uri $uri/ /index.html last;
		index index.html;
            }

            location /static {
                root /home/letterli/IT/Vue/ee-talk-backend/dist;
            }


	    location /thxt/api/ {
		add_header Access-Control-Allow-Origin *;
	        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
    	  	add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';

	        if ($request_method = 'OPTIONS') {
		    return 204;
	        }


                proxy_pass http://127.0.0.1:8080;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            }
        }

	server {
            listen          8081;
            server_name     ee.zju.edu.cn;

        }

	include /etc/nginx/conf.d/*.conf;
	include /etc/nginx/sites-enabled/*;
}

```

## 上传至服务器
用filezilla等工具、scp命令传输文件到服务器都可以。

另外，服务器中的数据库也要和本地的同步，否则flask程序启动时会检测到数据库异常等问题。

上述就是把网站部署到服务器的最简版本
## 杂记
这次部署虽然没啥太多东西，flask也不难。但是还是遇到了很多问题。归结起来是自己环境部署的时候没有在本地配置通过，因此服务器上也花费了很多时间。
### 感想1
以后还是要现在本地把项目用dev模式开发的差不多，准备部署试试的时候，先在本地把
1. nginx
2. vue生产环境模式
3. flask用gunicorn或者其他uwgsi生产服务器托起来
这样测试通过后把文件上传到服务器就没啥大问题了。

### 感想2
其中遇到一个问题是有两天部署上去不管怎么样api请求都是超时的，我查看F12其中的请求url，然后手动去访问也是一直没有反映。然后发现是因为自己的写法是：

在vue的生产环境配置中 base_url: url/api/

所以请求发起都是： url/api/userlist/……

而其实后端响应路径都是 url/userlist/……   相当于发出的请求都没有人处理

于是在后端程序每个响应路由前加上/api改成 /api/userlist就可以了