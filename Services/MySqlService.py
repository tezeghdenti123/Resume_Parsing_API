import time
class MySqlService:
    def getAllOpportunity(self,mysql):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM opportunite")
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