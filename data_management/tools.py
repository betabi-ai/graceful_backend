from shares.models import GsoneJancode


def _checkval(val, length):
    return len(val) == length


# GTIN（JAN代码） 标准型（13位）
def _getgtinjan13(val):
    """
    生成 GTIN（JAN代码） 标准型（13位）
    """
    if _checkval(val, 12):
        factor = 3
        total_sum = 0
        for index in range(len(val), 0, -1):
            total_sum += int(val[index - 1]) * factor
            factor = 4 - factor
        return val + str((1000 - total_sum) % 10)
    else:
        return ""


def generate_gs_one_jancodes(gs_prefix, start, end, user=None):
    datas = []
    for i in range(start, end + 1):
        gs_jancode = _getgtinjan13(f"{gs_prefix}{i:03}")
        if user:
            datas.append(
                GsoneJancode(
                    gs_prefix=gs_prefix,
                    gs_jancode=gs_jancode,
                    gs_index=i,
                    updated_by=user,
                )
            )
        else:
            datas.append(
                GsoneJancode(
                    gs_prefix=gs_prefix,
                    gs_jancode=gs_jancode,
                    gs_index=i,
                )
            )

    return datas
