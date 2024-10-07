from . import models

def getScore(schoolClass, week):
    try:
        return models.Score.objects.get(schoolClass=schoolClass, week=week)
    except models.Score.DoesNotExist:
        return None
    except models.Score.MultipleObjectsReturned:
        return None
    
def formatScoresForPdfTable(scores):
    formattedScores = [['Rang', 'Classe', 'Moyenne', 'Score nul', 'Score\nMathador']]
    i = 1
    for score in scores:
        formattedScores.append([i, score.schoolClass.name, score.numericScore, score.nullScoresPercentage, score.mathadorsPercentage])
        i += 1
    return formattedScores

def formatScoresForPdfPodium(scores):
    formattedRanking = [scores[0].schoolClass.name, scores[1].schoolClass.name, scores[2].schoolClass.name]
    return formattedRanking