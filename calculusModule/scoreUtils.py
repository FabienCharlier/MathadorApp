from . import models

def getScore(schoolClass, week):
    try:
        return models.Score.objects.get(schoolClass=schoolClass, week=week)
    except models.Score.DoesNotExist:
        return None
    except models.Score.MultipleObjectsReturned:
        return None
    
def areScoresEqual(score1, score2):
    return score1.numericScore == score2.numericScore and score1.nullScoresPercentage == score2.nullScoresPercentage and score1.mathadorsPercentage == score2.mathadorsPercentage
    
def formatClassDtosForPdfTable(scoreDtos):
    formattedScores = [['Rang', 'Classe', 'Moyenne', 'Score nul', 'Score\nMathador']]
    for scoreDto in scoreDtos:
        if scoreDto.score is None:
            formattedScores.append([scoreDto.ranking, scoreDto.schoolClass.name, '-', '-', '-'])
        else:
            formattedScores.append([scoreDto.ranking, scoreDto.schoolClass.name, round(scoreDto.score.numericScore, 2), round(scoreDto.score.nullScoresPercentage, 2), round(scoreDto.score.mathadorsPercentage, 2)])
    return formattedScores

def formatClassDtosForPdfPodium(scoreDtos):
    formattedRanking = [scoreDtos[0].schoolClass.name, scoreDtos[1].schoolClass.name, scoreDtos[2].schoolClass.name]
    return formattedRanking