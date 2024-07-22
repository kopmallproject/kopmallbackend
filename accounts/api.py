from typing import List

from django.shortcuts import get_object_or_404

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from accounts.models import User
from accounts.schema import (
    ERROR_403OUTSCHEMA,
    CreateUserOutSchema,
    UserInSchema,
    UserOutSchema,
)

router = Router(auth=JWTAuth())


@router.post(
    "register/",
    description="The endpoint creates a new user",
    response={201: CreateUserOutSchema},
    auth=None,
)
def register_user(request, payload: UserInSchema):
    return User.objects.create_user(**payload.dict())


@router.get(
    "/",
    description="The endpoint retrieves all user records",
    response={200: List[UserOutSchema]},
)
def list_users(request):
    return User.objects.all()


@router.get(
    "/me",
    description="The endpoint retrieves the logged in user records",
    response={200: UserOutSchema},
)
def me(request):
    return request.user


@router.get(
    "/{user_id}",
    description="The endpoint retrieves the user records by ID",
    response={200: UserOutSchema, 403: ERROR_403OUTSCHEMA},
)
def get_user(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    if request.user is not user:
        return 403, {"error": "Restriction!"}
    return user
