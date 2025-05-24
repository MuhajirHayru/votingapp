from django.urls import path
from .views import RegisterView, LoginView, CandidateList, VoteView

urlpatterns = [
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/candidates/', CandidateList.as_view()),
    path('api/vote/', VoteView.as_view()),
]
