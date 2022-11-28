import gridfs
from pymongo import MongoClient
from decouple import config
from bson.objectid import ObjectId


def connection():
    client = MongoClient(config('MONGODB_IP', cast=str),
                         config('MONGODB_PORT', cast=int))

    database = client.microservices

    grid_fs = gridfs.GridFS(database=database)

    return grid_fs
