from fishing_tournament import app
from fishing_tournament.config.mysqlconnection import connectToMySQL
from fishing_tournament.models import user_model
from flask import flash

class Submission:
    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.length = data['length']
        self.time_landed = data['time_landed']
        self.multiplier = data['multiplier']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.verified = data['verified']
        self.user_id = data['user_id']

    @classmethod
    def create_submission(cls, data):
        query = "INSERT INTO submissions (species, length, time_landed, multiplier, created_at, updated_at, verified, user_id) VALUES (%(species)s, %(length)s, %(time_landed)s, %(multiplier)s, NOW(), NOW(), 'false', %(user_id)s)"
        result = connectToMySQL('fishing_tournament').query_db(query, data)
        return result

    @classmethod
    def verify_submission(cls, data):
        query = "UPDATE submissions SET verified = 'true' WHERE id = %(id)s;"
        result = connectToMySQL('fishing_tournament').query_db(query, data)
        return result

    @classmethod
    def get_submissions_by_user_id(cls, data):
        query = "SELECT * FROM submissions WHERE user_id = %(id)s"
        result = connectToMySQL('fishing_tournament').query_db(query, data)
        return result

