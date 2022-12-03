from flask_app.config.mysqlconnection import connectToMySQL
import re	#regex thing
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash


class User:
    db_name = 'exam2'
    def __init__(self,data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    
    @classmethod
    def addUser(cls,data):
        query = 'INSERT INTO users ( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)

    
    @classmethod
    def getUserByID(cls,data):
        query = 'SELECT * FROM users WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results[0]

    @classmethod
    def getUserByEmail(cls,data):
        query = 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if results:
            return results[0]
        return False





    @staticmethod
    def validateUser(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters long", 'first_name') 
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters long", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(user['password']) < 8: 
            flash("Password must be at least 8 characters long!", 'passwordRegister')
            is_valid = False
        if user['password']!=user['confirmPassword']:
            flash("Passwords don't match, try again", 'passwordConfirm')
            is_valid = False
        return is_valid
