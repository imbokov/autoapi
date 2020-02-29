from django.db.models import *


class Post(Model):
    user = ForeignKey("auth.User", on_delete=PROTECT, related_name="posts")

    title = CharField(max_length=255)
    text = TextField()

    def __str__(self):
        return self.title


class Comment(Model):
    user = ForeignKey("auth.User", on_delete=PROTECT, related_name="comments")
    post = ForeignKey(Post, on_delete=PROTECT, related_name="comments")

    text = TextField()

    def __str__(self):
        return f"Comment {self.pk} by {self.user} for {self.post}"
