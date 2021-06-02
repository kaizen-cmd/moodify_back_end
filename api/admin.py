from django.contrib import admin
from api.models import *

# Register your models here.

admin.site.register(Song)
admin.site.register(SongMood)
admin.site.register(User)
admin.site.register(UserFollowing)
