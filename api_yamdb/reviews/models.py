from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from titles.models import Title
from users.models import User


class Reviews(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Rewiew"
        verbose_name_plural = "Rewiews"
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(fields=["title", "author"], name="unique_review")
        ]

    def __str__(self):
        return self.text[:30]


class Comments(models.Model):
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:30]
