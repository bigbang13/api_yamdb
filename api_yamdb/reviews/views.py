from api.serializers import CommentsSerializer, ReviewsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from titles.models import Title
from reviews.models import Reviews


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]    #TODO - проверить права

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]    #TODO - проверить права

    def get_review(self):
        return get_object_or_404(
            Reviews,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id")
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review_id=review.id)

    #TODO - добавить расчет средней оценки???
