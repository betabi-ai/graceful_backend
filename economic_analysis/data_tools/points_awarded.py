import csv
import chardet

from shares.models import PointsAwarded


def detect_encoding(file_path):
    """
    检测文件编码
    """
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


_HEADER_COLUMNS = ["日付", "付与件数", "付与ポイント"]

_COLUMNS_DICT = {
    "付与ポイント": "pointsawarded",
    "日付": "effectdate",
    "付与件数": "numbers",
}


def read_points_awardeds(file_path, shopid):
    with open(
        file_path,
        "r",
        encoding="SHIFT_JIS",
    ) as f:
        reader = csv.DictReader(f)

        header_row = reader.fieldnames
        if header_row == _HEADER_COLUMNS:
            datas = []
            dates = []
            for row in reader:
                mapped_row = {
                    _COLUMNS_DICT[key]: value
                    for key, value in row.items()
                    if key in _COLUMNS_DICT
                }
                pointsawarded = int(mapped_row["pointsawarded"].replace(",", ""))
                if pointsawarded <= 0:
                    break

                effectdate = mapped_row["effectdate"][:10].replace("/", "-")
                mapped_row["effectdate"] = effectdate
                dates.append(effectdate)
                mapped_row["shopid"] = shopid

                # print(effectdate, pointsawarded)
                datas.append(PointsAwarded(**mapped_row))

            PointsAwarded.objects.filter(shopid=shopid, effectdate__in=dates).delete()

            PointsAwarded.objects.bulk_create(datas)


if __name__ == "__main__":
    file_path = "/Users/kevincoder/Desktop/data/InvestList202411242.csv"
    # print(detect_encoding(file_path))

    # read_points_awardeds()
