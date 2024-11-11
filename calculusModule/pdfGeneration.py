from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from . import models, schoolClassUtils, scoreUtils

def buildFirstColumn(primaryTableData, collegeTableData):
    tableStyle = TableStyle([
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('VALIGN', (0,0), (-1, 0), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (0, -1), 'CENTER'),
        ('ALIGN', (2,0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    titleStyle = ParagraphStyle(name="titleStyle",fontName="Helvetica-Bold", spaceAfter=5)

    primaryTableTitle = Paragraph('<u>PRIMAIRES :</u>', style=titleStyle)
    primaryTable = Table(primaryTableData, colWidths=[50,250,60,60,60], style=tableStyle)
    spacer = Spacer(1,20)
    collegeTableTitle = Paragraph('<u>COLLEGE :</u>', style=titleStyle)
    collegeTable = Table(collegeTableData, colWidths=[50,250,60,60,60], style=tableStyle)
    return [primaryTableTitle,primaryTable, spacer, collegeTableTitle, collegeTable]

def buildSecondColumn(primaryRanking, collegeRanking):
    imagePath = "./calculusModule/static/podium.png"
    image = Image(imagePath, 150, 150)

    primaryRankingTableData = [["",primaryRanking[0],""],["","",primaryRanking[1]],[primaryRanking[2],"",""]]
    collegeRankingTableData = [["",collegeRanking[0],""],["","",collegeRanking[1]],[collegeRanking[2],"",""]]
    primaryRankingTable = Table(primaryRankingTableData)
    collegeRankingTable = Table(collegeRankingTableData)
    spacer = Spacer(1, 20)

    return [image, primaryRankingTable, spacer, image, collegeRankingTable]

def buildFullPage(width, week, primaryTableData, collegeTableData, primaryRanking, collegeRanking):
    titleStyle = ParagraphStyle(name="titleStyle",fontName="Helvetica-Bold", fontSize=14)
    title = Paragraph(f"<u>CLASSEMENT DU MATHADOR : SEMAINE {week.displayNumber} DU {week.dateStart.strftime('%d/%m/%Y')} au {week.dateEnd.strftime('%d/%m/%Y')}</u>", style=titleStyle)

    tablePartWidth = width * 2 / 3
    imagePartWidth = width * 1 / 3
    firstColumn = buildFirstColumn(primaryTableData, collegeTableData)
    secondColumn = buildSecondColumn(primaryRanking, collegeRanking)
    twoColumnsStyle = TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('VALIGN', (0,0), (-1, -1), 'TOP'),
    ])
    spacer = Spacer(1, 20)

    twoColumnsLayout = Table([[firstColumn, secondColumn]], colWidths=[tablePartWidth, imagePartWidth], style=twoColumnsStyle)
    return [title, spacer, twoColumnsLayout]

def buildPdf(buffer, week, primaryTableData, collegeTableData, primaryRanking, collegeRanking):
    width, height = landscape(A4)
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=(width,height),
        topMargin=10,
        leftMargin=15,
        rightMargin=15,
        bottomMargin=10,
    )
    pdf.build(buildFullPage(width - 30, week, primaryTableData, collegeTableData, primaryRanking, collegeRanking))

def generatePdf(currentWeek, buffer):
    cm2Level = models.SchoolClassLevel.CM2
    sixiemeLevel = models.SchoolClassLevel.SIXIEME

    sortedCm2ClassesDtos = schoolClassUtils.getSortedClassesForWeekAndLevel(currentWeek, cm2Level)
    sortedSixiemeClassesDtos = schoolClassUtils.getSortedClassesForWeekAndLevel(currentWeek, sixiemeLevel)
    
    cm2TableData = scoreUtils.formatClassDtosForPdfTable(sortedCm2ClassesDtos)
    cm2RankingData = scoreUtils.formatClassDtosForPdfPodium(sortedCm2ClassesDtos)
    sixiemeTableData = scoreUtils.formatClassDtosForPdfTable(sortedSixiemeClassesDtos)
    sixiemeRankingData = scoreUtils.formatClassDtosForPdfPodium(sortedSixiemeClassesDtos)

    buildPdf(buffer, currentWeek, cm2TableData, sixiemeTableData, cm2RankingData, sixiemeRankingData)