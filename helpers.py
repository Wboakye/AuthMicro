from app import db
from passlib.hash import pbkdf2_sha256 as sha256


class DbMethods:
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class RevokedToken(object):
    def __init__(self, jti):
        self.jti = jti
        self.db = db

    def add(self):
        self.db.revokedtokens.insert_one({ "jti" : self.jti })

    @classmethod
    #check for jti, return bool
    def is_jti_blacklisted(cls, jti):
        query = db.revokedtokens.find_one({"jti" : jti})
        return bool(query)