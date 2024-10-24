from typing import Any, List
from ninja.pagination import paginate, PaginationBase
from ninja import Schema


class CustomPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        skip: int

    class Output(Schema):
        items: List[Any]  # `items` is a default attribute
        total: int
        per_page: int

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        return {
            "items": queryset[skip : skip + 5],
            "total": queryset.count(),
            "per_page": 5,
        }
