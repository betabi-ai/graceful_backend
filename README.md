
在项目的根目录下运行：
  `docker-compose build -d`,可以直接将整个项目进行 docker 部署

清理未使用的镜像: `docker system prune`

生成token：
python -c "import secrets;print(secrets.token_urlsafe(54))"

查看发布了哪些spider:

<http://160.16.234.163:6800/listspiders.json?project=gracefulRakutenSpiders>

查看scrapyd spider log:
<http://160.16.234.163:6800/jobs>

<!-- {
  detail: '此令牌对任何类型的令牌无效',
  code: 'token_not_valid',
  messages: [
    {
      token_class: 'AccessToken',
      token_type: 'access',
      message: '令牌无效或已过期'
    }
  ]
} -->
