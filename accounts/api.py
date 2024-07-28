from typing import List

from django.shortcuts import get_object_or_404

from ninja import Router
from ninja_jwt.authentication import JWTAuth
from pydantic import EmailStr

from accounts.models import OTP, User
from accounts.schema import (
    CreateUserOutSchema,
    GetOTPInSchema,
    ResetPasswordInSchema,
    UserInSchema,
    UserOutSchema,
    VerifyOTPOutSchema,
)

from core.schema import(
    ERROR_403OUTSCHEMA,
    NOTFOUND_404OUTSCHEMA,
    SUCCESS_200OUTSCHEMA,
    SUCCESS_201OUTSCHEMA,
)

router = Router(auth=JWTAuth())


@router.post(
    "/forget-password",
    description="The endpoint for forget password",
    response={201: SUCCESS_201OUTSCHEMA},
    auth=None
)
def forget_password(request, payload: GetOTPInSchema):

    user = get_object_or_404(User, email__iexact=payload.email)

    OTP.otp_session(user=user)

    return 201, {'message': "OTP sent successfully"}

@router.post(
    "/verify-otp",
    description="The endpoint for verification of OTP codes",
    response={201: SUCCESS_201OUTSCHEMA, 404: NOTFOUND_404OUTSCHEMA},
    auth=None
)
def verify_otp(request, payload: VerifyOTPOutSchema):

    email = payload.email
    
    otp = payload.otp

    user = get_object_or_404(User, email__iexact=email)

    if not OTP.check_otp(user, otp):
        return 404, {'message': 'otp incorrect or expired, request another one'}

    # setting email verification field true.
    if not user.email_verified:
        user.email_verified = True
        user.save()

    return 201, {'message': 'account successfully verified'}

@router.post(
    "/register",
    description="The endpoint creates a new user",
    response={201: CreateUserOutSchema},
    auth=None,
)
def register_user(request, payload: UserInSchema):
    return User.objects.create_user(**payload.dict())

@router.put(
    "/reset-password",
    description="The endpoint for resetting password",
    response={200: SUCCESS_200OUTSCHEMA},
    auth=None
)
def reset_password(request, payload: ResetPasswordInSchema):

    user = get_object_or_404(User, email__iexact=payload.email)
    user.set_password(payload.password)
    user.save()

    return 200, {'message': 'password reset successfully'}

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
    if request.user != user:
        return 403, {"error": "Restriction!"}
    return user

@router.get(
    "/{email}/get-otp",
    description="The endpoint to get verification OTP codes",
    response={200: SUCCESS_200OUTSCHEMA},
    auth=None
)
def get_otp(request, email: EmailStr):

    user = get_object_or_404(User, email__iexact=email)

    if user.email_verified:
        return 200, {'message': 'account already been verified'}

    OTP.otp_session(user=user)  # send OTP to user

    return 200, {'message': 'otp sent to your mail'}