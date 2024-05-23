from Services.MySqlService import MySqlService
from Models.Statistics import Statistic
from Models.Location import Location
from Models.Duree import Duree
from Models.Titre import Titre
class StatisticService:
    def getStatistic(self,mysql):
        mysqlService=MySqlService()
        nbNewOppor=mysqlService.getNumberOfNewOpportunite(mysql)
        tjm=mysqlService.getTjmStatistics(mysql)
        durr=mysqlService.getContractDurationOccurence(mysql)
        listDuration=[Duree(durr[0][0],durr[0][1]).__dict__,Duree(durr[1][0],durr[1][1]).__dict__,Duree(durr[2][0],durr[2][1]).__dict__,Duree(durr[3][0],durr[3][1]).__dict__]
        
        loc=mysqlService.getLocationOccurence(mysql)
        medtjm=mysqlService.getTjmMediane(mysql)
        titre=mysqlService.getTendanceTitle(mysql)
        listLocation=[Location(loc[0][0],loc[0][1]).__dict__,Location(loc[1][0],loc[1][1]).__dict__,Location(loc[2][0],loc[2][1]).__dict__,Location(loc[3][0],loc[3][1]).__dict__,Location(loc[4][0],loc[4][1]).__dict__,Location(loc[5][0],loc[5][1]).__dict__]
        titre=Titre(titre[0][0],titre[0][1])
        statistic=Statistic(nbNewOppor[0][0],tjm[0][0],float(tjm[0][1]),tjm[0][2],medtjm[0][0],listLocation,listDuration,titre.__dict__)
        return  statistic.__dict__
    
    def Test(self,mysql):
        mysqlService=MySqlService()
        for i in range(30):
            mysqlService.saveTjmMediane(mysql,550)
        
        for i in range(30):
            mysqlService.saveTjmMediane(mysql,550)
        for i in range(20):
            mysqlService.saveTjmMediane(mysql,630)

