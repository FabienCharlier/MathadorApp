from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('add-score/<int:classId>', views.addScore, name="addScore"),
    path('edit-score/<int:scoreId>', views.editScore, name="editScore"),
    path('delete-score/<int:scoreId>', views.deleteScore, name="deleteScore"),
    path('weekly-scores', views.weeklyScores, name="weeklyScores"),
    path('downloadWeeklyScorePdf', views.downloadWeeklyScorePdf, name="downloadWeeklyScorePdf"),
    path('all-time-scores', views.allTimeScores, name="allTimeScores"),
    path('downloadAllTimePdf', views.downloadAllTimePdf, name="downloadAllTimePdf"),
    path('emails', views.emails, name="emails"),
    path('sendEmails/reminder', views.sendEmailsReminder, name="sendEmailsReminder"),
    path('sendEmails/newWeek', views.sendEmailsNewWeek, name="sendEmailsNewWeek"),
    path('sendEmails/results', views.sendEmailsResults, name="sendEmailsResults")
]