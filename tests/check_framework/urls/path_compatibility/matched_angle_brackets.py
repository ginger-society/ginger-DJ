from gingerdj.urls import path

urlpatterns = [
    path("<int:angle_bracket>", lambda x: x),
]
