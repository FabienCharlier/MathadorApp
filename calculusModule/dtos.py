class SchoolClassWithRankingAndScore:
    def __init__(self, schoolClass, score, ranking):
        self.schoolClass = schoolClass
        self.score = score
        self.ranking = ranking

class ScoreDto:
    def __init__(self, numericScore, nullScoresPercentage, mathadorsPercentage):
        self.numericScore = numericScore
        self.nullScoresPercentage = nullScoresPercentage
        self.mathadorsPercentage = mathadorsPercentage