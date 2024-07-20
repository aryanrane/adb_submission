from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import os
from pymongo import MongoClient
from bson import ObjectId

# MongoDB connection
mongo_uri = f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"
client = MongoClient(mongo_uri)
db = client['test_db']
todo_collection = db['todo']

class TodoListView(APIView):

    def get(self, request):
        try:
            # Fetching data
            todos = list(todo_collection.find())
            for todo in todos:
                todo['_id'] = str(todo['_id'])
            return Response(todos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        # Ensure the request is JSON
        if request.content_type != 'application/json':
            return Response({"error": "Unsupported Media Type. Please use application/json."},
                            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
        try:
            # Handle JSON data
            todo_data = request.data

            # Clearing all existing data from Mongo
            todo_collection.delete_many({})
            
            # Insert the new TODO item into the MongoDB collection
            if todo_data:
                todo_collection.insert_one(todo_data)
            
            # Fetch the newly inserted TODO items from the MongoDB collection
            todos = list(todo_collection.find())
            for todo in todos:
                todo['_id'] = str(todo['_id'])
            
            return Response(todos, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
