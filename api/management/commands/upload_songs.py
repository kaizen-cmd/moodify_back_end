from django.core.management.base import BaseCommand, CommandError
import os
from django.core.files import File
from api.models import Song, SongMood
from django.conf import settings

class Command(BaseCommand):

    help = "Upload Songs"

    def handle(self, *args, **options):

        try:
            BASE_DIR = settings.BASE_DIR
            songs_dir = BASE_DIR / "Moodify_Songs"
            dirs = os.listdir(songs_dir)
            dirs.remove("venv")
            dirs.remove("chromedriver")
            dirs.remove("try.py")
            dirs.remove("cover.jpg")
            mod = [songs_dir / i for i in dirs]

            for j in mod:
                p = os.listdir(j)
                for k in p:
                        c = j / k
                        ff = os.listdir(c)
                        if len(ff) != 1:
                                cover = open(c / ff[0], "rb")
                                mp3 = open(c /ff[1], "rb")
                                d_c = File(cover)
                                d_m = File(mp3)
                                dg = str(c).split("/")[-2].capitalize()
                                sm = SongMood.objects.filter(mood=dg).first()
                                print(sm, dg)
                                sg = Song()
                                sg.name = ff[1].split(".")[0]
                                sg.save()
                                sg.mood.add(sm.pk)
                                sg.mp3_file.save(ff[1], d_m, save=True)
                                sg.poster.save("cover.jpg", d_c, save=True)
        except Exception as e:
            raise CommandError(str(e))

