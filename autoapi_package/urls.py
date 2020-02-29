from typing import List, Type

from django.apps import apps
from django.db.models import Model
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.routers import BaseRouter, SimpleRouter
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .conf import autoapi_settings
from .constants import (
    ROUTER_KEY,
    SERIALIZER_CLASS_KEY,
    VIEWSET_CLASS_KEY,
    URL_PREFIX_KEY,
)
from .utils import get_model_key

router: BaseRouter = autoapi_settings.get(ROUTER_KEY, SimpleRouter())

models: List[Model] = apps.get_models()

for model in models:
    opts = model._meta

    model_settings: dict = autoapi_settings.get(get_model_key(opts), {})

    if SERIALIZER_CLASS_KEY in model_settings:
        serializer_class: Type[Serializer] = model_settings[SERIALIZER_CLASS_KEY]
    else:

        class AutoSerializer(ModelSerializer):
            class Meta:
                model = model
                fields = "__all__"

        serializer_class = AutoSerializer

    if VIEWSET_CLASS_KEY in model_settings:
        viewset_class: Type[GenericViewSet] = model_settings[VIEWSET_CLASS_KEY]
    else:

        class AutoViewSet(ModelViewSet):
            queryset = opts.default_manager.all()
            serializer_class = serializer_class
            pagination_class = LimitOffsetPagination
            filter_backends = [OrderingFilter, SearchFilter]

        viewset_class = AutoViewSet

    url_prefix = model_settings.get(URL_PREFIX_KEY, opts.model_name)
    router.register(url_prefix, viewset_class)

urlpatterns = router.urls
