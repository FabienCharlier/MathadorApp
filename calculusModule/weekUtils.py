from . import models

def getLastWeek():
    return models.Week.objects.order_by('dateStart').last()