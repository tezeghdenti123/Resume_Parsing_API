import time
class MySqlService:
    def getAllOpportunity(self,mysql):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id,titre,description,date,tjm,duree,location FROM opportunite")
        data = cur.fetchall()
        cur.close()
        return data
    def saveOpportunity(self,mysql,titre,desc,date,tjm,dure,location):
        query = "INSERT INTO opportunite (titre, description,date,tjm,duree,location) VALUES (%s, %s,%s,%s,%s,%s)"

        try:
            # Execute the query
            cur = mysql.connection.cursor()
            cur.execute(query, (titre, desc,date,tjm,dure,location))
            mysql.connection.commit()
            cur.close()
            print('Data inserted successfully')
            return 'Data inserted successfully'
        except Exception as e:
            print(e)
            return str(e)
        
    def deleteAllOpportunity(self,mysql):
        try:
            # Create SQL DELETE query
            query = "DELETE FROM opportunite"

            # Execute the query
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            cur.close()

            return 'All data deleted successfully'
        except Exception as e:
            return str(e)
        

    def updateDataBase(self,mysql,titre,desc,date,tjm,dure,location):
        self.deleteAllOpportunity(mysql)
        time.sleep(5)
        self.saveOpportunity(mysql,titre,desc,date,tjm,dure,location)
    
    def getLocationOccurence(self,mysql):
        cur = mysql.connection.cursor()
        nb=6
        cur.execute("select location,count(*) as occurrence from opportunite group by location order by occurrence desc limit %s",(nb,))
        data = cur.fetchall()
        cur.close()
        return data
    
    def getContractDurationOccurence(self,mysql):
        cur = mysql.connection.cursor()
        nb=4
        cur.execute("select duree,count(*) as occurrence from opportunite group by duree order by occurrence desc limit %s",(nb,))
        data = cur.fetchall()
        cur.close()
        return data
    
    def getTjmStatistics(self,mysql):
        cur = mysql.connection.cursor()
        cur.execute("select min(tjm) as min,avg(tjm) as avg,max(tjm) as max from opportunite")
        data = cur.fetchall()
        cur.close()
        return data
    
    def getNumberOfNewOpportunite(self,mysql):
        cur = mysql.connection.cursor()
        cur.execute("select count(*) from opportunite where date not like '%jours%'")
        data = cur.fetchall()
        cur.close()
        return data
    
    def getTjmMediane(self,mysql):
        cur = mysql.connection.cursor()
        cur.execute("with rankedValues as( select tjm, row_number() over(order by tjm) as row_num, count(*) over() as total_count from opportunite) select avg(tjm) as median from rankedValues where row_num in (floor((total_count+1)/2),ceil((total_count+1)/2))")
        data = cur.fetchall()
        cur.close()
        return data
    
    def saveTjmMediane(self,mysql,medtjm):
        query = "INSERT INTO statistics (medtjm) VALUES (%s)"

        try:
            # Execute the query
            cur = mysql.connection.cursor()
            cur.execute(query, (medtjm,))
            mysql.connection.commit()
            cur.close()
            print('Data inserted successfully')
            return 'Data inserted successfully'
        except Exception as e:
            print(e)
            return str(e)
    

    def getTendanceTitle(self,mysql):
        cur = mysql.connection.cursor()
        nb=1
        cur.execute("select titre,count(*) as occurrence from opportunite group by titre order by occurrence desc limit %s",(nb,))
        data = cur.fetchall()
        cur.close()
        return data