import django.shortcuts as shortcuts
import django.http as http
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required

from . import forms, weekUtils, scoreUtils, models

@login_required
def index(request):
    lastWeek = weekUtils.getLastWeek()
    allClasses = models.SchoolClass.objects.filter(teacher=request.user)
    for schoolClass in allClasses:
        schoolClass.score = scoreUtils.getScore(schoolClass, lastWeek)
    return shortcuts.render(request, "calculusModule/index.html", {'lastWeek': lastWeek, 'allClasses': allClasses})

def login(request):
    if request.method == 'POST':
        loginForm = forms.LoginForm(request.POST)
        if loginForm.is_valid():
            email = loginForm.cleaned_data['email']
            user = auth.models.User.objects.get(email=email)
            auth.login(request, user)
            return shortcuts.redirect('index')
    else:
        loginForm = forms.LoginForm()
    return shortcuts.render(request, "calculusModule/login.html", {'form': loginForm})

def logout(request):
    auth.logout(request)
    return shortcuts.redirect('login')

@login_required
def addScore(request, classId):
    scoreSchoolClass = models.SchoolClass.objects.get(id=classId)
    lastWeek = weekUtils.getLastWeek()
    if request.method == 'POST':
        addScoreForm = forms.AddScoreForm(request.POST)
        if addScoreForm.is_valid():
            newScore = addScoreForm.save(commit=False)
            newScore.week = lastWeek
            newScore.schoolClass = scoreSchoolClass
            newScore.save()
            return shortcuts.redirect('index')
    else:
        addScoreForm = forms.AddScoreForm()
    return shortcuts.render(request, "calculusModule/addScore.html", {'form': addScoreForm, 'schoolClass': scoreSchoolClass, 'lastWeek': lastWeek})

@login_required
def editScore(request, scoreId):
    previousScore = models.Score.objects.get(pk=scoreId)
    if request.method == 'POST':
        print('PATCH detected')
        addScoreForm = forms.AddScoreForm(request.POST)
        if addScoreForm.is_valid():
            newScore = addScoreForm.save(commit=False)
            models.Score.objects.filter(pk=scoreId).update(numericScore=newScore.numericScore, nullScoresPercentage=newScore.nullScoresPercentage, mathadorsPercentage=newScore.mathadorsPercentage)
            return shortcuts.redirect('index')
    else:
        print('PATCH not detected')
        addScoreForm = forms.AddScoreForm(instance=previousScore)
    return shortcuts.render(request, "calculusModule/editScore.html", {'form': addScoreForm, 'previousScore': previousScore})

@login_required
def deleteScore(request, scoreId):
    if request.method == 'POST':
        models.Score.objects.filter(pk=scoreId).delete()
        return shortcuts.redirect('index')
    else:
        previousScore = models.Score.objects.get(pk=scoreId)
    return shortcuts.render(request, "calculusModule/deleteScore.html", {'score': previousScore})

def weeklyScores(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        raise http.Http404
    lastWeek = weekUtils.getLastWeek()
    cm2Level = models.SchoolClassLevel.CM2
    cm2LevelScores = models.Score.objects.filter(week=lastWeek, schoolClass__level=cm2Level).order_by('-numericScore','nullScoresPercentage','-mathadorsPercentage')
    sixiemeLevel = models.SchoolClassLevel.SIXIEME
    sixiemeLevelScores = models.Score.objects.filter(week=lastWeek, schoolClass__level=sixiemeLevel).order_by('-numericScore','nullScoresPercentage','-mathadorsPercentage')

    return shortcuts.render(request, "calculusModule/weeklyScores.html", {'cm2OrderedScores': cm2LevelScores, '6eOrderedScores': sixiemeLevelScores, 'lastWeek': lastWeek})