from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class SongMood(models.Model):

    MOOD_CHOICES = (
        ("Happy", "Happy"),
        ("Sad", "Sad"),
        ("Angry", "Angry"),
        ("Surprised", "Surprised"),
        ("Neutral", "Neutral")
    )

    mood = models.CharField(choices=MOOD_CHOICES, max_length=50)

    def __str__(self):

        return self.mood


class Song(models.Model):

    name = models.CharField(max_length=150)
    artist = models.CharField(max_length=150, blank=True, null=True)
    duration = models.CharField(max_length=10)
    poster = models.ImageField(upload_to="song_posters")
    mp3_file = models.FileField(upload_to="song_files")
    mood = models.ManyToManyField(to=SongMood, related_name="songs")

    def __str__(self):
        return self.name

class User(AbstractUser):

    groups = None

    MOOD_CHOICES = (
        ("Happy", "Happy"),
        ("Sad", "Sad"),
        ("Angry", "Angry"),
        ("Surprised", "Surprised"),
        ("Neutral", "Neutral")
    )

    mood = models.CharField(max_length=150, choices=MOOD_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)

    def __str__(self) -> str:

        return str(self.pk) + self.username


class UserFollowing(models.Model):

    user_id = models.ForeignKey(to=User, related_name="following", on_delete=models.CASCADE, blank=True, null=True)

    following_user_id = models.ForeignKey(to=User, related_name="followers", on_delete=models.CASCADE, blank=True, null=True)

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user_id.username if self.user_id else 'None' + " is " + " followed by " + self.following_user_id.usernmae if self.following_user_id else 'None'