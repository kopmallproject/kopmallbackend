from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

from ninja import NinjaAPI
from ninja import Swagger
from ninja_jwt.routers.obtain import obtain_pair_router
from ninja_extra import exceptions

from accounts.api import router as accounts_router
from stores.api import router as stores_router


api = NinjaAPI(docs=Swagger())

api.add_router("/users/", accounts_router)
api.add_router("/stores/", stores_router)
api.add_router("/token", tags=["Auth"], router=obtain_pair_router)

urlpatterns = [path("admin/", admin.site.urls), path("api/", api.urls)]


def api_exception_handler(request, exc):
    headers = {}

    if isinstance(exc.detail, (list, dict)):
        data = exc.detail
    else:
        data = {"detail": exc.detail}

    response = api.create_response(request, data, status=exc.status_code)
    for k, v in headers.items():
        response.setdefault(k, v)

    return response


api.exception_handler(exceptions.APIException)(api_exception_handler)

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
