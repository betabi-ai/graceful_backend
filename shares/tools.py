from django.db import connection


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
