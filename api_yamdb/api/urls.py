from django.urls import include, path
from rest_framework.routers import DefaultRouter
from reviews.views import CommentViewSet, ReviewViewSet
from .views import SignUpAPIView, UserAPIView

app_name = "api"

router = DefaultRouter()

router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/users/", UserAPIView.as_view()),
    path("v1/auth/signup/", SignUpAPIView.as_view()),
]
