from . import models, dtos, scoreUtils

def getSortedClassesForWeekAndLevel(week, level):
    scores = models.Score.objects.filter(week=week, schoolClass__level=level).order_by('-numericScore','nullScoresPercentage','-mathadorsPercentage')
    classesWithoutScore = models.SchoolClass.objects.filter(level=level).exclude(score__week=week)

    rankedClassDtos = []
    visibleRank = 1
    actualRank = 1
    previousScore = None

    for score in scores:
        if previousScore is None or scoreUtils.areScoresEqual(score, previousScore) == False:
            visibleRank = actualRank
        schoolClassDtoWithRankingAndScore = dtos.SchoolClassWithRankingAndScore(score.schoolClass, score, visibleRank)
        rankedClassDtos.append(schoolClassDtoWithRankingAndScore)

        actualRank += 1
        previousScore = score

    for classWithoutScore in classesWithoutScore:
        schoolClassDtoWithRankingAndScore = dtos.SchoolClassWithRankingAndScore(classWithoutScore, None, actualRank)
        rankedClassDtos.append(schoolClassDtoWithRankingAndScore)

    return rankedClassDtos