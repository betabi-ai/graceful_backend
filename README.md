
在项目的根目录下运行：
  `docker-compose build -d`,可以直接将整个项目进行 docker 部署

生成token：
python -c "import secrets;print(secrets.token_urlsafe(54))"

查看发布了哪些spider:

<http://160.16.234.163:6800/listspiders.json?project=gracefulRakutenSpiders>

查看scrapyd spider log:
<http://160.16.234.163:6800/jobs>
