from django.contrib import admin

from .models import Comments, Reviews


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "text",
        "author",
        "score",
        "pub_date",
    )
    search_fields = ("text", "author__username")
    list_filter = ("score", "pub_date")
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "review",
        "text",
        "author",
        "pub_date",
    )
    search_fields = ("text", "author__username")
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


admin.site.register(Reviews, ReviewAdmin)
admin.site.register(Comments, CommentAdmin)
