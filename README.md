# autoapi

## Introduction

This is a proof of concept, and not a distributable package. The repository is a regular django project. `autoapi_package` folder is what can be made distributable eventually.

## Usage

Usage example:
```python
# urls.py

from autoapi_package import urlpatterns as autoapi_urls

urlpatterns = [
    # ...
    path("autoapi/", include(autoapi_urls)),
]
```

Now this path has api endpoints for all models in your project.

The default configuration is:
* `SimpleRouter` for a router
* `model_name` as a `url_prefix` for the router
* `ModelSerializer` with fields set to `__all__`
* `ModelViewSet` with a default manager's queryset and:
    * `LimitOffsetPagination` as pagination
    * `OrderingFilter` with all fields allowed
    * `DjangoFilterBackend` where all fields can be filtered upon

If you wish to override any of those settings, here's an example:

```python
# settings.py

AUTOAPI = {
    "ROUTER": DefaultRouter(),
    "forum.comment": {
        "viewset_class": "forum.views.CommentViewSet",
        "url_prefix": "comments",
        # "serializer_class": ...,
    },
}
```
