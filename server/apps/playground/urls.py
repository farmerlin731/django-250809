from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server.apps.playground.views import (
    HiView,
    ItemDetailView,
    ItemListView,
    ItemViewSet,  # Version 4 - include list & detail
    hello,
)

router = DefaultRouter(trailing_slash=False)
# When u meet 'viewset'
# U should register router by this way
router.register("items-v2", ItemViewSet)

urlpatterns = [
    path("hello", hello),
    path("hi", HiView.as_view()),
    path("items", ItemListView.as_view()),
    path("items/<int:pk>", ItemDetailView.as_view()),
    path("viewset/", include(router.urls)),  # u also can make the path blank
]
