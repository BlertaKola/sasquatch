from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Sighting:
    db_name = 'exam2'
    def __init__(self,data):
        self.id = data['id'],
        self.location = data['location'],
        self.description = data['description'],
        self.dateSight = data['dateSight'],
        self.numberSasq = data['numberSasq'],
        self.user_id = data['user_id'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    
    @classmethod
    def addReport(cls,data):
        query = 'INSERT INTO sightings ( location, description, dateSight, numberSasq, user_id ) VALUES ( %(location)s, %(description)s, %(dateSight)s, %(numberSasq)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)
    

    @classmethod
    def getReportByID(cls,data):
        query = 'SELECT * FROM sightings WHERE sightings.id = %(sighting_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results[0]
    
    

    @classmethod
    def getAllReports(cls):
        query = 'SELECT sightings.location, sightings.id, sightings.dateSight, users.first_name as creator_name, users.id as creator_id FROM sightings LEFT JOIN users ON sightings.user_id = users.id;'
        results = connectToMySQL(cls.db_name).query_db(query)
        return results


    @classmethod
    def believUnbelieve(cls,data):
        query = 'SELECT sighting_id as id FROM sceptics LEFT JOIN users ON sceptics.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        believers = []
        for row in results:
            believers.append(row['id'])
        return believers






    @classmethod
    def deleteReport(cls,data):
        query = 'DELETE FROM sightings WHERE sightings.id = %(sighting_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod      #delete
    def deleteBelievers(cls,data):
        query = 'DELETE FROM sceptics WHERE sceptics.sighting_id = %(sighting_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)






    @classmethod
    def getScepticsCount(cls,data):
        query = 'SELECT count(sceptics.id) AS number FROM sceptics LEFT JOIN sightings ON sceptics.sighting_id = sightings.id LEFT JOIN users on sceptics.user_id = users.id WHERE sceptics.user_id = %(user_id)s GROUP BY sightings.id;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return 0


    @classmethod
    def getSceptics(cls,data):
        query = 'SELECT users.first_name FROM sceptics LEFT JOIN users ON sceptics.user_id = users.id WHERE sighting_id = %(sighting_id)s GROUP BY user_id;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        sceptics = []
        for row in result:
            sceptics.append(row)
        return sceptics

    @classmethod
    def updateReport(cls,data):
        query = 'UPDATE sightings SET location = %(location)s, description = %(description)s, dateSight = %(dateSight)s, numberSasq = %(numberSasq)s, user_id = %(user_id)s WHERE id = %(id)s; '
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def believeReport(cls,data):
        query = 'INSERT INTO sceptics ( sighting_id, user_id ) VALUES ( %(sighting_id)s, %(user_id)s ); '
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def unbelieveReport(cls,data):
        query = 'DELETE FROM sceptics WHERE sighting_id = %(sighting_id)s AND user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)


    
    @staticmethod
    def validateReport(report):
        is_valid = True
        if len(report['location']) < 1:
            flash("Location is required", 'location')
            is_valid = False
        if len(report['description']) < 1:
            flash("The description of what happened is required", 'description')
            is_valid = False
        if report['dateSight'] == '':
            flash("The date of report is required", 'dateSight')
            is_valid = False
        if report['numberSasq'] == '' :
            flash("The minimum of Sasquatches is 1", 'numberSasq')
            is_valid = False
        return is_valid 