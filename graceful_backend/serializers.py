from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 添加用户信息到 token 中
        token["username"] = user.username
        token["email"] = user.email

        return token

    def validate(self, attrs):
        print("...........................", attrs)
        data = super().validate(attrs)

        # 在响应数据中添加用户信息
        data.update(
            {
                "user": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "email": self.user.email,
                }
            }
        )

        return data
