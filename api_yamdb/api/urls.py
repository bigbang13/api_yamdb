from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SignUpAPIView

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet,
)

app_name = "api"

router = DefaultRouter()

router.register(r"titles", TitleViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews")
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", SignUpAPIView.as_view()),
]
