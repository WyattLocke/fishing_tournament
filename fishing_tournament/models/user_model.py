from fishing_tournament import app
from fishing_tournament.config.mysqlconnection import connectToMySQL
from fishing_tournament.models import submission_model
from operator import itemgetter,attrgetter
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.division = data['division']
        self.guided_unguided = data['guided_unguided']
        self.admin = data['admin']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.submissions = []

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 3:
            is_valid = False
            flash("First name must be at least 3 characters.", "registration")
        if len(data['last_name']) < 3:
            is_valid = False
            flash("Last name must be at least 3 characters.", "registration")
        if User.get_by_email(data):
            flash("Email already taken.", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address.", "registration")
            is_valid = False
        if len(data['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.", "registration")
        if data['confirm_password'] != data['password']:
            is_valid = False
            flash("Passwords don't match.", "registration")
        return is_valid

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, division, guided_unguided, admin, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(division)s, %(guided_unguided)s, %(admin)s, NOW(), NOW());"
        result = connectToMySQL('fishing_tournament').query_db(query, data)
        print(result)
        return result

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        result = connectToMySQL('fishing_tournament').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s"
        result = connectToMySQL('fishing_tournament').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_users_with_submissions_by_division_gu(cls, data):
        query = "SELECT * FROM users LEFT JOIN submissions ON users.id = submissions.user_id WHERE division = %(division)s AND guided_unguided = %(guided_unguided)s;"
        results = connectToMySQL('fishing_tournament').query_db(query, data)
        
        users = []
        user_ids = []

        for user in results:
            if user['id'] not in user_ids:
                user_ids.append(user['id'])
                users.append(cls(user))
            submission_data = {
                "id" : user['submissions.id'],
                "species" : user['species'],
                "length" : user['length'],
                "time_landed" : user['time_landed'],
                "multiplier" : user['multiplier'],
                "created_at" : user['submissions.created_at'],
                "updated_at" : user['submissions.updated_at'],
                "verified" : user['verified'],
                "user_id" : user['user_id']
            }
            users[len(users) - 1].submissions.append(submission_model.Submission(submission_data))

        return users

# Copy of above method with an added filter for verified submissions
    @classmethod
    def get_users_with_submissions_by_division_gu_verified(cls, data):
        query = "SELECT * FROM users LEFT JOIN submissions ON users.id = submissions.user_id WHERE division = %(division)s AND guided_unguided = %(guided_unguided)s AND verified = 'true';"
        results = connectToMySQL('fishing_tournament').query_db(query, data)
        
        users = []
        user_ids = []

        for user in results:
            if user['id'] not in user_ids:
                user_ids.append(user['id'])
                users.append(cls(user))
            submission_data = {
                "id" : user['submissions.id'],
                "species" : user['species'],
                "length" : user['length'],
                "time_landed" : user['time_landed'],
                "multiplier" : user['multiplier'],
                "created_at" : user['submissions.created_at'],
                "updated_at" : user['submissions.updated_at'],
                "verified" : user['verified'],
                "user_id" : user['user_id']
            }
            users[len(users) - 1].submissions.append(submission_model.Submission(submission_data))

        return users


    # logic for calculating scores for users
    @classmethod
    def get_users_with_submissions_scores(cls, data):
        # gets all users with all submissions
        users = cls.get_users_with_submissions_by_division_gu_verified(data)

        for u in users:
            # create intermediate dictionary for filtering submissions
            sub_scores = {
                "Tarpon": [],
                "Snook": [],
                "Redfish": []
            }
            # calculate score for each submission and filter
            for s in u.submissions:
                sub_data = {
                    "id": s.id,
                    "score": float(s.length * s.multiplier)
                }
                print(sub_data)
                sub_scores[s.species].append(sub_data)
                print(sub_scores)

            total_score = 0
            for key in sub_scores:
                # returns the object with the max value in the attribute 'score', and overwrites the value in the sub_score directory (previously the list) with the max score value for that species
                print("List to iterate", sub_scores[key])
                # checks that is not empty
                if sub_scores[key]:
                    sub_scores[key] = max(sub_scores[key], key=itemgetter('score'))
                else:
                    sub_scores[key] = {'score': 0.0}
                print(f"total_score = {total_score}, sub_scores[key] = {sub_scores[key]}, sub_scores[key]['score'] = {sub_scores[key]['score']}")
                total_score += sub_scores[key]['score']

            u.total_score = total_score

        print(users)
        users = sorted(users, key=attrgetter('total_score'), reverse = True)
        return users





