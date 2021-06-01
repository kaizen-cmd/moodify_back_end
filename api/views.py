from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from api.models import *
import base64
from moodifymodel.recog3 import class_labels, return_mood
import os
from .models import Song, SongMood, User
from argparse import Namespace
from django.core.files import File

def get_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:

        ip = x_forwarded_for.split(',')[0]

    else:

        ip = request.META.get('REMOTE_ADDR')

    return ip


class MoodDetectViewSet(ViewSet):

    BASE_URL = "https://583cc35d272c.ngrok.io"

    def log_user(self, request):

        data = request.data

        data = Namespace(**data)

        name = data.name

        ip_addr = get_ip(request)

        if not User.objects.filter(name=name).exists():

            User.objects.create(name=name, ip_addr=ip_addr)

        return Response({"result": "Success"})

    def view_users(self, request):

        ip_addr = get_ip(request)

        curr_user = User.objects.filter(ip_addr=ip_addr).first()

        users = User.objects.all()

        users_dict = [
            {
                "id": user.pk,
                "name": user.name,
                "mood": user.mood,
                "image": f"{self.BASE_URL if user.image else 'https://img.icons8.com/color/96/000000/circled-user-male-skin-type-1-2--v1.png'}{user.image.url if user.image else ''}",
                "is_following": user.followers.filter(pk=curr_user.pk).exists()
            } for user in users]

        return Response(users_dict)

    def view_followers(self, request):

        ip_addr = get_ip(request)

        followers_dict ={}

        user = User.objects.filter(ip_addr=ip_addr).first()

        if user:

            followers = user.followers.all()

            followers_dict = [{"name": follower.name, "mood": follower.mood} for follower in followers]

        return Response(followers_dict)

    def follow_user(self, request):

        ip_addr = get_ip(request)

        data = request.data

        data = Namespace(**data)

        user = User.objects.filter(ip_addr=ip_addr).first()

        context = {"result": "Failure"}

        if user:

            user_to_be_followed = User.objects.filter(pk=data.id).first()

            if user_to_be_followed:

                user_to_be_followed.followers.add(user)

                user.following.add(user_to_be_followed)

                context["result"] = "Success"

        return Response(context)

    def view_following(self, request):

        ip_addr = get_ip(request)

        user = User.objects.filter(ip_addr=ip_addr).first()

        following_dict = {}

        if user:

            followers = user.following.all()

            following_dict = [{"name": follower.name, "mood": follower.mood} for follower in followers]

        return Response(following_dict)

    def image_analysis(self, request):
        ip_addr = get_ip(request)
        songs = []
        mood = "Error try again"

        data = request.data
        image_data = data.get("image", None)
        if image_data:
            image_data = image_data.split(',')[1]
            image_data = base64.b64decode(image_data)
            file_name = "media/mood_image.jpg"
            with open(file_name, 'wb') as f:
                f.write(image_data)

            '''

            Integrate the ML model

            '''

            model_op = return_mood(file_name)
            if isinstance(model_op, int):

                mood = class_labels[int(model_op)]
                song_mood_obj = SongMood.objects.filter(mood=mood).first()

                if song_mood_obj:

                    song_qs = Song.objects.filter(mood__in=[song_mood_obj])
                    songs = [{"id": song.pk, "name": song.name, "singer": song.artist, "cover": f"{self.BASE_URL}{song.poster.url}",
                              "musicSrc": f"{self.BASE_URL}{song.mp3_file.url}"} for song in song_qs]

                    user = User.objects.filter(ip_addr=ip_addr).first()

                    if user:
                        user.mood = mood
                        try:
                            img = File(file_name)
                            user.image.save(user.pk, img, save=True)
                        except Exception as e:
                            pass
                        user.save()

        return Response({"mood": mood, "songs": songs})
