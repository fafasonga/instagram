import time
import imageio
import pandas as pd
import matplotlib.pyplot as plt
from InstagramAPI import InstagramAPI
from tqdm import tqdm

imageio.plugins.ffmpeg.download()

username = "fafasonga06"
password = "Fafastar05"
InstagramAPI = InstagramAPI(username, password)
InstagramAPI.login()

InstagramAPI.getProfileData()
result = InstagramAPI.LastJson
username = result['user']['username']   # username = "Diana"
# print(result)
# print(username)
# print(result['user']['biography'])

InstagramAPI.timelineFeed()

myposts = []
max_id = ""
followers = []
has_more_posts = True
next_max_id = True

while has_more_posts:
    InstagramAPI.getSelfUserFeed(maxid=max_id)
    if InstagramAPI.LastJson['more_available'] is not True:
        has_more_posts = False  # stop condition
        print("Processing Finished")

    max_id = InstagramAPI.LastJson.get('next_max_id', '')
    myposts.extend(InstagramAPI.LastJson['items'])  # merge lists
    time.sleep(1)  # Slows the script down to avoid flooding the servers

datas = []
for k in myposts:
    likes_counts = k['like_count']
    datas.append(likes_counts)
    top_likers = k['top_likers']
    # print(top_likers)

InstagramAPI.getRecentActivity()
get_recent_activity_response = InstagramAPI.LastJson

InstagramAPI.getProfileData()
user_id = InstagramAPI.LastJson['user']['pk']

InstagramAPI.getUserFollowings(user_id)
following_list = InstagramAPI.LastJson['users']
InstagramAPI.getUserFollowers(user_id)
followers_list = InstagramAPI.LastJson['users']

while next_max_id:
    #first iteration hack
    if next_max_id == True:
        next_max_id = ''
    _ = InstagramAPI.getUserFollowers(user_id, maxid=next_max_id)
    followers.extend(InstagramAPI.LastJson.get('users', []))
    next_max_id = InstagramAPI.LastJson.get('next_max_id', '')
    time.sleep(1)

followers_list = followers

user_list = map(lambda x: x['username'], following_list)
following_set = set(user_list)

user_list = map(lambda x: x['username'], followers_list)
followers_set = set(user_list)

not_following_back = following_set - followers_set
fans = followers_set - following_set
print("\nNumber of Followers: ", len(followers_set))
print("Number of Following: ", len(following_set))
print("Number of Not Following back: ", len(not_following_back))
print("Number of Fans: ", len(fans))
print("\nPeople that do not Follow me back: ", not_following_back)
# print("\nfollowing: ", following_set)

# print(datas)
plt.plot(datas)
fig = plt.gcf()
plt.ylabel('Number of Likes')
plt.title('Display of Instagram Likes for my Profile')
fig.savefig("Counts_of_Likes")
plt.show()

for notification in get_recent_activity_response['old_stories']:
    text = notification['args']['text']
    if username in text:
        print("\nText: ", text)
