from django.urls import path
from api import views

image_analysis = views.MoodDetectViewSet.as_view({
    'post': 'image_analysis'
})

log_user = views.MoodDetectViewSet.as_view({
    'post': 'log_user'
})

view_users = views.MoodDetectViewSet.as_view({
    'get': 'view_users'
})

view_followers = views.MoodDetectViewSet.as_view({
    'get': 'view_followers'
})

view_following = views.MoodDetectViewSet.as_view({
    'get': 'view_following'
})

follow_user = views.MoodDetectViewSet.as_view({
    'post': 'follow_user'
})

urlpatterns = [
    path("post-image/", image_analysis),
    path("log-user/", log_user),
    path("view-users/", view_users),
    path("view-followers/", view_followers),
    path("view-following/", view_following),
    path("follow-user/", follow_user)
]
