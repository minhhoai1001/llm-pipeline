import json

from bson import json_util
from data_cdc.config import settings
from core.db.mongo import MongoDBClient
from core.mq import publish_to_rabbitmq

def stream_process():
    try:
        print("Connected to MongoDB.")
        client = MongoDBClient()
        db = client["CaptionDB"]

        # Watch changes in a specific collection
        changes = db.watch([{"$match": {"operationType": {"$in": ["insert"]}}}])
        for change in changes:
            data_type = change["ns"]["coll"]
            entry_id = str(change["fullDocument"]["_id"])  # Convert ObjectId to string

            change["fullDocument"].pop("_id")
            change["fullDocument"]["type"] = data_type
            change["fullDocument"]["entry_id"] = entry_id

            if data_type not in ["articles", "posts", "repositories"]:
                print(f"Unsupported data type: '{data_type}'")
                continue

            # Use json_util to serialize the document
            data = json.dumps(change["fullDocument"], default=json_util.default)
            print(
                f"Change detected and serialized for a data sample of type {data_type}."
            )

            # Send data to rabbitmq
            publish_to_rabbitmq(queue_name=settings.RABBITMQ_QUEUE_NAME, data=data)
            print(f"Data of type '{data_type}' published to RabbitMQ.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        stream_process()