from django.urls import path

import upload_case

urlpatterns = [
    path('blog',upload_case.view.upload),
]
