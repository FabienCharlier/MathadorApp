def reminderMailSubject(currentWeek):
    return f'Rappel : Mathador - Résultats de la {currentWeek.fullInlineDisplay()}'

def newWeekMailSubject(currentWeek):
    return f'Mathador - Tirage de la {currentWeek.fullInlineDisplay()}'

def resultsMailSubject(currentWeek):
    return f'Mathador - Résultats de la {currentWeek.fullInlineDisplay()}'