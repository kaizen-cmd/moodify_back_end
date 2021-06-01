from django.db import models

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

class User(models.Model):

    MOOD_CHOICES = (
        ("Happy", "Happy"),
        ("Sad", "Sad"),
        ("Angry", "Angry"),
        ("Surprised", "Surprised"),
        ("Neutral", "Neutral")
    )

    name = models.CharField(max_length=150)
    mood = models.CharField(max_length=150, choices=MOOD_CHOICES, blank=True, null=True)
    followers = models.ManyToManyField(to='self', related_name='foll', blank=True)
    following = models.ManyToManyField(to='self', related_name='foll2', blank=True)
    ip_addr = models.GenericIPAddressField()
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)

    def add_follower(self):

        pass

    def __str__(self):

        return self.name + " " + str(self.pk)
