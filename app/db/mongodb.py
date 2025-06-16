from injector import inject
from pymongo import MongoClient

YOUTUBE_VIDEO_COLLECTION = 'youtube_videos'
PIPELINE_COLLECTION = 'pipelines'


class Db:
    @inject
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client['admin']

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def get_db(self):
        return self.db

    def get_client(self):
        return self.client

    def get_youtube_video_item_by_id(self, video_id):
        return self.get_collection(YOUTUBE_VIDEO_COLLECTION).find_one({'video_id': video_id})

    def insert_or_update_pipeline_item(self, pipeline_object):
        self.get_collection(PIPELINE_COLLECTION).update_one(
            {'video_id': pipeline_object.video_id},
            {'$set': pipeline_object.to_dict()},
            upsert=True
        )

    def get_pipeline_item_by_id(self, video_id):
        return self.get_collection(PIPELINE_COLLECTION).find_one({'video_id': video_id})
