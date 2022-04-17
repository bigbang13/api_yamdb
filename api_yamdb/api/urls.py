from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SignUpAPIView
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet,
    UserViewSet,
    CustomTokenObtainPairView,
)

app_name = "api"

router = DefaultRouter()

router.register(r"titles", TitleViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"categories", CategoryViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register("users", UserViewSet)

urlpatterns = [
    path("v1/auth/signup/", SignUpAPIView.as_view()),
    path("v1/", include(router.urls)),
    path(
        "v1/auth/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
]
