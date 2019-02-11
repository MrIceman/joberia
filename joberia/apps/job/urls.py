from django.urls import path

from .views import JobView, CommentView

urlpatterns = [
    path('', JobView.as_view(), name='job_view'),
    path('comment', CommentView.as_view(), name='comment_view')

]
