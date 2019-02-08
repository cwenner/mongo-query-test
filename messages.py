import random
import statistics
import string

from pymongo import MongoClient

client = MongoClient()
client.drop_database("maven")
db = client.maven

# Populate db

num_groups = 1000
num_users = 10000
user_per_group = 30
messages_per_user = 10
randstr = lambda: "".join(random.sample(string.ascii_letters, 16))

user_ids = db.User.insert_many(
    [dict(username=randstr()) for _ in range(num_users)]
).inserted_ids
group_ids = db.Group.insert_many(
    [dict(user_ids=random.sample(user_ids, user_per_group)) for _ in range(num_groups)]
).inserted_ids
db.Message.insert_many(
    [
        #dict(author_id=random.choice(user_ids), body=randstr())
        dict(group_id=random.choice(group_ids), body=randstr())
        for _ in range(num_users)
        for _ in range(messages_per_user)
    ]
)

def eval_query(query):
    print(
        "Query exec time (ms):",
        query.explain()["executionStats"]["executionTimeMillis"],
    )

def get_user_messages(user_id):
    return db.Message.find({"author_id": user_id})

eval_query(get_user_messages(random.choice(user_ids)))
