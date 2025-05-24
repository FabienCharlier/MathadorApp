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

def getSortedClassesAllTimeForLevel(level):
    all_classes_with_scores = models.SchoolClass.objects.filter(level=level).prefetch_related(
        models.Prefetch('score_set', queryset=models.Score.objects.all())
    )

    for class_with_scores in all_classes_with_scores:
        all_scores = class_with_scores.score_set.all()
        numeric_scores = [numeric_score for numeric_score in all_scores.values_list('numericScore', flat=True) if numeric_score is not None]
        if numeric_scores:
            class_with_scores.average_numeric_score = sum(numeric_scores) / len(numeric_scores)
        else:
            class_with_scores.average_numeric_score = None
        null_percentage_scores = [null_percentage_score for null_percentage_score in all_scores.values_list('nullScoresPercentage', flat=True) if null_percentage_score is not None]
        if null_percentage_scores:
            class_with_scores.average_null_percentage_score = sum(null_percentage_scores) / len(null_percentage_scores)
        else:
            class_with_scores.average_null_percentage_score = None
        mathador_percentage_scores = [mathador_percentage_score for mathador_percentage_score in all_scores.values_list('mathadorsPercentage', flat=True) if mathador_percentage_score is not None]
        if mathador_percentage_scores:
            class_with_scores.average_mathador_percentage_score = sum(mathador_percentage_scores) / len(mathador_percentage_scores)
        else:
            class_with_scores.average_mathador_percentage_score = None

    all_classes_with_scores = sorted(all_classes_with_scores, key=lambda x: (x.average_numeric_score or 0, -1 * (x.average_null_percentage_score or 1000), x.average_mathador_percentage_score or 0), reverse=True)

    rankedClassDtos = []
    actualRank = 1

    for class_with_scores in all_classes_with_scores:
        scoreDto = dtos.ScoreDto(class_with_scores.average_numeric_score, class_with_scores.average_null_percentage_score, class_with_scores.average_mathador_percentage_score)
        schoolClassDtoWithRankingAndScore = dtos.SchoolClassWithRankingAndScore(class_with_scores, scoreDto, actualRank)
        rankedClassDtos.append(schoolClassDtoWithRankingAndScore)

        actualRank += 1

    return rankedClassDtos