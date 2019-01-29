import time
import imageio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from InstagramAPI import InstagramAPI


imageio.plugins.ffmpeg.download()

username = "fafasonga06"
password = "Fafastar05"
InstagramAPI = InstagramAPI(username, password)
InstagramAPI.login()

InstagramAPI.getProfileData()
result = InstagramAPI.LastJson
username = result['user']['username']
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
    # first iteration hack
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

followerz = []
for follower in followers_set:
    followerz.append(follower)

followingz = []
for following in following_set:
    followingz.append(following)

fanz = []
for fann in fans:
    fanz.append(fann)

not_followingz = []
for not_following in not_following_back:
    not_followingz.append(not_following)

l1 = followerz
l2 = fanz
l3 = followingz
l4 = not_followingz

s1 = pd.Series(l1, name='Followers')
s2 = pd.Series(l2, name='Fans')
s3 = pd.Series(l3, name='Following')
s4 = pd.Series(l4, name='Not Following')

df = pd.concat([s1, s2, s3, s4], axis=1)
df.to_csv('insta_analysis.csv', sep=';', encoding='utf-8')

likerz = []
for g in myposts:
    likes_counts = np.array(g['like_count'])
    top_likers = np.array(g['top_likers'])
    for j in top_likers:
        likerz.append(j)

d = {x: likerz.count(x) for x in likerz}
x_axis, y_axis = d.keys(), d.values()

fig = plt.figure(figsize=(50, 30))
plt.plot(x_axis, y_axis)
plt.bar(x_axis, y_axis)
plt.xticks(rotation='vertical')
plt.title('Display of Instagram Likes for my Profile')
plt.xlabel('USERS')
plt.ylabel('Number of liked posts')
fig.savefig("Insta_Analysis")
plt.show()

plt.gcf().clear()

fig1, ax1 = plt.subplots(figsize=(30, 40))
ax1.pie(y_axis, labels=x_axis, autopct='%1.1f%%',
        shadow=False, startangle=-40)
ax1.axis('equal')
ax1.set_xticklabels(x_axis, rotation=90)
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax1.set_title("Display of Instagram Likes for my Profile")
fig1.savefig('Insta_analysispi.png', bbox_inches='tight')
plt.show()

fig, ax = plt.subplots(figsize=(50, 30), subplot_kw=dict(aspect="equal"))

recipe = list(x_axis)
data = y_axis

wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1) / 2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})

    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                horizontalalignment=horizontalalignment, **kw)
ax.set_title("Display of Instagram Likes for my Profile")
fig.savefig('Insta_analysispie.png', bbox_inches='tight')
plt.show()

for notification in get_recent_activity_response['old_stories']:
    text = notification['args']['text']
    if username in text:
        print("\nText: ", text)
