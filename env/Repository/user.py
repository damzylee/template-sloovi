from pymongo import MongoClient
from bson import json_util, ObjectId
import json
import os
from dotenv import load_dotenv

load_dotenv()


class UserRepository:

    def __init__(self):
        self.client = MongoClient(os.environ.get('MONGO_URI'))
        self.db = self.client.template_database
        self.users = self.db.user_collection

    def get_id(self, user_id):
        user = self.users.find_one({"_id": ObjectId(user_id)})
        user = json.loads(json_util.dumps(user))
        user["_id"] = user["_id"]["$oid"]
        return user

    def get_email(self, email):
        user = self.users.find_one({"email": email})
        user = json.loads(json_util.dumps(user))
        user["_id"] = user["_id"]["$oid"]
        return user

    def get_all(self):
        cursor = self.users.find({})
        users = list(cursor)
        users = json.loads(json_util.dumps(users))
        for item in users:
            item["_id"] = item["_id"]["$oid"]
        return users

    def save(self, user):
        persisted_user = self.users.insert_one(user)
        new_id = json.loads(json_util.dumps(persisted_user.inserted_id))
        return list(new_id.values())[0]

    def update(self, user):
        user_id = user["_id"]
        del user["_id"]
        result = self.users.update_one(filter={"_id": ObjectId(user_id)}, update={"$set": user})
        return result.modified_count

    def delete(self, user):
        result = self.users.delete_one({"_id": ObjectId(user)})
        return result.deleted_count