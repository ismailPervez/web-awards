from email.policy import default
from turtle import title
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=150)
    desc = models.TextField(max_length=250)
    preview_image = CloudinaryField('image', default='https://images.pexels.com/photos/1779487/pexels-photo-1779487.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='', editable=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def get_reviews(self):
        reviews = Review.objects.filter(post=self).all()
        return reviews

    def is_rated(self, current_user):
        rating = Rating.objects.filter(post=self, user=current_user).first()
        if rating:
            return True
        return False

    def get_avg_ratings(self):
        post_ratings = Rating.objects.filter(post=self).all()
        avg_ratings = 0
        for rating in post_ratings:
            avg_ratings += int(rating.value)

        if avg_ratings != 0:
            avg_ratings = avg_ratings / len(post_ratings)

        return avg_ratings

class Review(models.Model):
    content = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Rating(models.Model):
    value = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)