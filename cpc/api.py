from datetime import datetime
from typing import List
from ninja import Router, Schema
from ninja_jwt.authentication import JWTAuth

from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from cpc.models import CpcGoodKeywords
from cpc.schemas import CpcGoodKeywordsSchema

router = Router()


@router.get("/")
def index(request):
    return {"message": "Hello World"}


from pydantic import BaseModel


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None
    date_joined: datetime = None


@router.get(
    "/me",
    response=UserSchema,
)
def me(request):
    return request.user


@router.get("/keywords", response=List[CpcGoodKeywordsSchema], auth=None)
def get_keywords(request):
    qs = CpcGoodKeywords.objects.all()
    print(qs)
    return qs


@router.get("/keywords/{int:keyword_id}", response=CpcGoodKeywordsSchema, auth=None)
def get_keyword(request, keyword_id: int):
    qs = get_object_or_404(CpcGoodKeywords, id=keyword_id)
    return qs
