import json
import csv
import os
from truthbrush import Api
api = Api()

posts= api.trending()


groups = api.trending_groups()
groups.extend(api.suggested_groups())   
suggested_users = api.suggested()
users = []
users.extend(suggested_users)
# Fetching group posts

for group in groups:
    group_posts = api.group_posts(group["id"])

print(len(posts))

# Fetching suggested users posts and followers/followings

for user in suggested_users:
    print(user)
    user_followings = api.user_following(user_id=user["account"]["id"])
    user_followers = api.user_followers(user_id=user["account"]["id"])
    users.extend(user_followings)
    users.extend(user_followers)

for user in users:
    try:
        user_posts = api.pull_statuses(user_id=user["id"])
    except KeyError:
        user_posts = api.pull_statuses(user_id=user["account"]["id"])
    posts.extend(user_posts)
new_users = []
# Pull comments and like for each post and add them to the posts list
for post in posts:
    comments = api.pull_comments(post["id"], include_all=True)
    likes = api.user_likes(post["id"])
    new_users.extend(likes)
    posts.extend(comments)

# On répète le processus pour les nouveaux utilisateurs trouvés
# et on ajoute leurs posts à la liste des posts

final_users = []
final_users.extend(new_users)
for user in new_users:
    try:
        user_followings = api.user_following(user_id=user["id"])
        user_followers = api.user_followers(user_id=user["id"])
    except KeyError:
        user_followings = api.user_following(user_id=user["account"]["id"])
        user_followers = api.user_followers(user_id=user["account"]["id"])
    final_users.extend(user_followings)
    final_users.extend(user_followers)

for user in final_users:
    try:
        user_posts = api.pull_statuses(user_id=user["id"])
    except KeyError:
        user_posts = api.pull_statuses(user_id=user["account"]["id"])
    posts.extend(user_posts)


with open("posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)
