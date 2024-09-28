from . import models

def getScore(schoolClass, week):
    try:
        return models.Score.objects.get(schoolClass=schoolClass, week=week)
    except models.Score.DoesNotExist:
        return None
    except models.Score.MultipleObjectsReturned:
        return None