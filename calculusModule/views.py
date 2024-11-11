import io
import urllib
import django.shortcuts as shortcuts
import django.http as http
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from . import forms, weekUtils, scoreUtils, models, pdfGeneration, schoolClassUtils, mailContent

def adminUserRequired(func):
    def wrapperAdminUserRequired(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated or not request.user.is_staff:
            raise http.Http404
        return func(*args, **kwargs)

    return wrapperAdminUserRequired

def redirectWithParams(url, params=None):
    response = shortcuts.redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response

def createTemplateParamsWithFlashes(request, templateParams):
    if 'success' in request.GET:
        templateParams['successMessage'] = request.GET['success']
    if 'warning' in request.GET:
        templateParams['warningMessage'] = request.GET['warning']
    if 'error' in request.GET:
        templateParams['errorMessage'] = request.GET['error']
    return templateParams

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
        addScoreForm = forms.AddScoreForm(request.POST)
        if addScoreForm.is_valid():
            newScore = addScoreForm.save(commit=False)
            models.Score.objects.filter(pk=scoreId).update(numericScore=newScore.numericScore, nullScoresPercentage=newScore.nullScoresPercentage, mathadorsPercentage=newScore.mathadorsPercentage)
            return shortcuts.redirect('index')
    else:
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

@adminUserRequired
def weeklyScores(request):
    lastWeek = weekUtils.getLastWeek()
    cm2Level = models.SchoolClassLevel.CM2
    sixiemeLevel = models.SchoolClassLevel.SIXIEME
    
    sortedCm2ClassesDtos = schoolClassUtils.getSortedClassesForWeekAndLevel(lastWeek, cm2Level)
    sortedSixiemeClassesDtos = schoolClassUtils.getSortedClassesForWeekAndLevel(lastWeek, sixiemeLevel)

    return shortcuts.render(request, "calculusModule/weeklyScores.html", {'sortedCm2ClassesDtos': sortedCm2ClassesDtos, 'sortedSixiemeClassesDtos': sortedSixiemeClassesDtos, 'lastWeek': lastWeek})

@adminUserRequired
def downloadPdf(request):
    lastWeek = weekUtils.getLastWeek()

    buffer = io.BytesIO()
    pdfGeneration.generatePdf(lastWeek, buffer)
    buffer.seek(0)

    return http.FileResponse(buffer, as_attachment=True, filename=f"resultats-semaine-{lastWeek.displayNumber}-mathador.pdf")

@adminUserRequired
def emails(request):
    if 'newWeekMailFormCurrentNumbers' in request.session:
        newWeekMailFormCurrentNumbers = request.session['newWeekMailFormCurrentNumbers']
    else:
        newWeekMailFormCurrentNumbers = "Tirage de la semaine"
    if 'newWeekMailFormPersonnalizedText' in request.session:
        newWeekMailFormPersonnalizedText = request.session['newWeekMailFormPersonnalizedText']
    else:
        newWeekMailFormPersonnalizedText = "Texte personnalisé"
    newWeekMailForm = forms.NewWeekMailForm({
        'currentNumbers': newWeekMailFormCurrentNumbers,
        'personnalizedText': newWeekMailFormPersonnalizedText
    })

    if 'resultsMailFormPersonnalizedText' in request.session:
        resultsMailFormPersonnalizedText = request.session['resultsMailFormPersonnalizedText']
    else:
        resultsMailFormPersonnalizedText = "Texte personnalisé"
    resultsMailForm = forms.ResultsMailForm({
        'personnalizedText': resultsMailFormPersonnalizedText,
    })

    templateParams = {'newWeekMailForm': newWeekMailForm, 'resultsMailForm': resultsMailForm}

    return shortcuts.render(request, "calculusModule/emails.html", createTemplateParamsWithFlashes(request, templateParams))

@adminUserRequired
def sendEmailsReminder(request):
    try:
        currentWeek = weekUtils.getLastWeek()
        classesWithoutScore = models.SchoolClass.objects.exclude(score__week=currentWeek)

        teachersEmail = set()
        for classWithoutScore in classesWithoutScore :
            teachersEmail.add(classWithoutScore.teacher.email)
        
        htmlMessage = render_to_string('calculusModule/htmlEmails/reminderMail.html')
        plainMessage = strip_tags(htmlMessage)
        email = EmailMultiAlternatives(
            mailContent.newWeekMailSubject(currentWeek),
            plainMessage,
            settings.EMAIL_HOST_USER,
            list(teachersEmail),
        )
        email.attach_alternative(htmlMessage, "text/html")
        email.send()

        return redirectWithParams('emails', {'success': 'Les rappels ont bien été envoyés'})
    except Exception as e:
        errorMessage = f"Une erreur est survenue lors de l'envoi des mails de rappel : {str(e)}"
        return redirectWithParams('emails', {'error': errorMessage})