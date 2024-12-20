停掉原来的django 项目：
之前项目的管理都是通过 `/data/app/conf/supervisord.conf`文件进行。

```sh
/data/app/.envs/gracefulmonster/bin/supervisorctl -c /data/app/conf/supervisord.conf stop all
```

在项目的根目录下运行：`docker-compose build -d`, 可以直接将整个项目进行 docker 部署。

清理未使用的镜像: `docker system prune`

生成token：
python -c "import secrets;print(secrets.token_urlsafe(54))"

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
