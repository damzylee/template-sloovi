from pymongo import MongoClient
from bson import json_util, ObjectId
import json
import os
from dotenv import load_dotenv

load_dotenv()


class TemplateRepository:

    def __init__(self):
        mongoUrl = "mongodb+srv://damzylee:pythonExample2022@cluster0.rsm44.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(mongoUrl)
        self.db = self.client.template_database
        self.templates = self.db.template_collection

    def get_id(self, template_id):
        template = self.templates.find_one({"_id": ObjectId(template_id)})
        template = json.loads(json_util.dumps(template))
        template["_id"] = template["_id"]["$oid"]
        return template

    def get_all(self):
        cursor = self.templates.find({})
        templates = list(cursor)
        templates = json.loads(json_util.dumps(templates))
        for item in templates:
            item["_id"] = item["_id"]["$oid"]
        return templates

    def save(self, template):
        persisted_template = self.templates.insert_one(template)
        new_id = json.loads(json_util.dumps(persisted_template.inserted_id))
        return list(new_id.values())[0]

    def update(self, template):
        template_id = template["_id"]
        del template["_id"]
        result = self.templates.update_one(filter={"_id": ObjectId(template_id)}, update={"$set": template})
        return result.modified_count

    def delete(self, template):
        result = self.templates.delete_one({"_id": ObjectId(template)})
        return result.deleted_count