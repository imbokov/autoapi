from django.apps import apps
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.routers import SimpleRouter
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .conf import autoapi_settings
from .constants import (
    ROUTER_KEY,
    SERIALIZER_CLASS_KEY,
    URL_PREFIX_KEY,
    VIEWSET_CLASS_KEY,
)
from .utils import get_class, get_field_names, get_model_key

router = autoapi_settings.get(ROUTER_KEY, SimpleRouter())

models = apps.get_models()

for model in models:
    opts = model._meta

    model_settings = autoapi_settings.get(get_model_key(opts), {})

    if SERIALIZER_CLASS_KEY in model_settings:
        serializer_class = get_class(model_settings[SERIALIZER_CLASS_KEY])
    else:

        class AutoSerializer(ModelSerializer):
            class Meta:
                model = model
                fields = "__all__"

        serializer_class = AutoSerializer

    if VIEWSET_CLASS_KEY in model_settings:
        viewset_class = get_class(model_settings[VIEWSET_CLASS_KEY])
    else:

        class AutoViewSet(ModelViewSet):
            queryset = opts.default_manager.all()
            serializer_class = serializer_class
            pagination_class = LimitOffsetPagination
            filter_backends = [DjangoFilterBackend, OrderingFilter]
            filterset_fields = get_field_names(opts)

        viewset_class = AutoViewSet

    url_prefix = model_settings.get(URL_PREFIX_KEY, opts.model_name)
    router.register(url_prefix, viewset_class)

urlpatterns = router.urls
