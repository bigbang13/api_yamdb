from django.urls import include, path
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpAPIView, TitleViewSet, UserViewSet)
=======
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet,
    UserViewSet,
    CustomTokenObtainPairView,
    SignUpAPIView,
)
>>>>>>> 4d48381da56ada90b83de15cabb1ba6f7a248ea1

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
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", SignUpAPIView.as_view()),
    path(
        "v1/auth/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
]
