import json
import csv
import os
from truthbrush import Api
api = Api()

posts= api.trending()

api.pull_comments(posts[0]["id"], include_all=True)
groups = api.trending_groups()
groups.extend(api.suggested_groups())   
suggested_users = api.suggested()
users = []
users.extend(suggested_users)

# Fetching group posts



# Fetching suggested users posts and followers/followings
try:
    for group in groups:
        group_posts = api.group_posts(group["id"])

    print(len(posts))

except Exception as e:
    print(e)
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2) 

with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2) 
