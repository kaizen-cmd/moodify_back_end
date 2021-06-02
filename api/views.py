from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core.files import File
from django.contrib.auth import authenticate

import base64
from argparse import Namespace

from api.models import *
from moodifymodel.recog3 import class_labels, return_mood

# def get_ip(request):

#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

#     if x_forwarded_for:

#         ip = x_forwarded_for.split(',')[0]

#     else:

#         ip = request.META.get('REMOTE_ADDR')

#     return ip


class MoodDetectViewSet(ViewSet):

    BASE_URL = "http://localhost:8000"

    def signup(self, request):

        data = request.data

        data = Namespace(**data)

        try:

            user = User.objects.create(
                email=data.email, username=data.username)

            user.set_password(data.password)

            user.save()

            Token.objects.get_or_create(user=user)

            return Response({"result": "Success"}, status=status.HTTP_200_OK)

        except Exception as e:

            print(e)

            return Response({"result": "Failure"}, status=status.HTTP_226_IM_USED)

    def login(self, request):

        data = request.data

        data = Namespace(**data)

        try:

            user = authenticate(
                request, username=data.username, password=data.password)

            if user != None:

                token = Token.objects.filter(user=user).first()

                if token:

                    return Response({"result": "Success", "token": token.key, "username": token.user.username, "pk": user.pk}, status=status.HTTP_200_OK)

        except Exception as e:

            print(e)

            return Response({"result": "Failure"}, status=status.HTTP_401_UNAUTHORIZED)

    def view_users(self, request):

        data = request.data

        data = Namespace(**data)

        token = Token.objects.filter(key=data.token).first()

        if token:

            curr_user = token.user

            users = User.objects.all().exclude(pk=curr_user.pk)

            users_dict = []

            for user in users:
                
                is_following = curr_user.following.filter(following_user_id=user).exists()

                user_dict = {
                    "id": user.pk,
                    "name": user.username,
                    "mood": user.mood,
                    "image": f"{self.BASE_URL if user.image else 'https://img.icons8.com/color/96/000000/circled-user-male-skin-type-1-2--v1.png'}{user.image.url if user.image else ''}",
                    "is_following": is_following
                }

                users_dict.append(user_dict)

            return Response(users_dict)
        
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def view_followers(self, request):

        data = request.data

        data = Namespace(**data)

        token = Token.objects.filter(key=data.token).first()

        user = token.user

        if user:

            followers = user.followers.all()
            dx = []

            for follower_id in followers:

                user = follower_id.user_id

                if user:

                    dx.append({"name": user.username, "mood": user.mood})

        return Response(dx)

    def follow_user(self, request):

        data = request.data

        data = Namespace(**data)

        token = Token.objects.filter(key=data.token).first()

        user = token.user

        context = {"result": "Failure"}

        if user:

            user_to_be_followed = User.objects.filter(pk=data.id).first()

            if user_to_be_followed:

                if not UserFollowing.objects.filter(
                        user_id=user, following_user_id=user_to_be_followed).exists():

                    UserFollowing.objects.create(
                        user_id=user, following_user_id=user_to_be_followed)

                context["result"] = "Success"

        return Response(context)

    def view_following(self, request):

        data = request.data

        data = Namespace(**data)

        token = Token.objects.filter(key=data.token).first()

        user = token.user

        following_dict = {}

        if user:

            followers = user.following.all()

            following_dict = [{"name": follower.user_id.username,
                               "mood": follower.user_id.mood} for follower in followers]

        return Response(following_dict)

    def image_analysis(self, request):
        data = request.data
        data = Namespace(**data)
        token = data.token
        token = Token.objects.filter(key=token).first()
        songs = []
        mood = "Error try again"

        if token:

            image_data = data.image
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

                        user = token.user

                        if user:
                            user.mood = mood
                            try:
                                img = File(file_name)
                                user.image.save(user.pk, img, save=True)
                            except Exception as e:
                                pass
                            user.save()

        return Response({"mood": mood, "songs": songs})
