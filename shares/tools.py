import chardet
from django.db import connection
from ninja.files import UploadedFile


# 根据SQL查询语句和参数获取结果
def get_result_with_sql(sql_query, params):
    """
    根据SQL查询语句和参数获取结果
    :param sql_query: SQL查询语句
    :param params: 参数
    :return: 查询结果
    """
    # 执行查询
    with connection.cursor() as cursor:

        cursor.execute(sql_query, params)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

        return results

    return []


def detect_file_encoding(file: UploadedFile):
    # 读取上传文件的全部内容
    raw_data = file.file.read()
    # 使用 chardet 检测编码
    result = chardet.detect(raw_data)
    encoding = result["encoding"]
    # 重置文件指针，确保后续操作可以继续读取文件内容
    file.file.seek(0)
    return encoding
