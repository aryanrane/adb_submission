from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from bson import ObjectId
import os

class MongoDBClient:
    def __init__(self):
        mongo_uri = f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"
        self.client = MongoClient(mongo_uri)
        self.db = self.client['test_db']
        self.collection = self.db['todo']

    def get_all_todos(self):
        return list(self.collection.find())

    def insert_todo(self, todo_data):
        self.collection.insert_one(todo_data)

    def clear_all_todos(self):
        self.collection.delete_many({})

class TodoListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mongo_client = MongoDBClient()

    def get(self, request):
        try:
            todos = self.mongo_client.get_all_todos()
            for todo in todos:
                todo['_id'] = str(todo['_id'])
            return Response(todos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        if request.content_type != 'application/json':
            return Response({"error": "Unsupported Media Type. Please use application/json."}, 
                            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        try:
            todo_data = request.data
            self.mongo_client.clear_all_todos()
            if todo_data:
                self.mongo_client.insert_todo(todo_data)
            todos = self.mongo_client.get_all_todos()
            for todo in todos:
                todo['_id'] = str(todo['_id'])
            return Response(todos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
