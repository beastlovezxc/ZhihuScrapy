import ZHLogin
from bs4 import BeautifulSoup
import json
from urllib.request import urlretrieve
import Zhihuer
import ZHDatabase
import re


user_url = 'https://www.zhihu.com/people/'
session = ZHLogin.login()
db = ZHDatabase.db


def chooseVersion(userID, dbName):
    userInfo = Zhihuer.Zhihuer()
    response = session.get(user_url + userID, headers=ZHLogin.headers)
    soup = BeautifulSoup(response.content, 'lxml')
    name = soup.find_all('span', {'class': 'name'})
    if name == []:
        response = session.get(user_url + userID +
                               '/followers', headers=ZHLogin.headers)
    # print(user_url + userID + '/followers')
        soup = BeautifulSoup(response.content, 'lxml')
        if soup.find('span', {'class': 'ProfileHeader-name'}) != None:
            userInfo = getUserInfoInNewVersion(userID)
    else:
        userInfo = getUserInfoInOldVersion(userID)
    saveUserInfotoDB(userInfo, dbName)


def getFollowingInNewVersion(userID):
    following_url = 'http://www.zhihu.com/people/' + userID + '/following'
    fileName = userID + '.txt'
    f = open('Following/' + fileName, 'w')
    response = session.get(following_url, headers=ZHLogin.headers)
    soup = BeautifulSoup(response.content, 'lxml')
    total = soup.findAll('div', {'class': 'Profile-followStatusValue'})[0].text
    getFollowing_url = 'https://www.zhihu.com/api/v4/members/' + userID + \
        '/followees?per_page=10&include=data%5B%2A%5D.employments%2Ccover_url%2Callow_message%2Canswer_count%2Carticles_count%2Cfavorite_count%2Cfollower_count%2Cgender%2Cis_followed%2Cmessage_thread_token%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=10&offset='

    times = int(int(total) / 10)
    # print(times)
    for i in range(1, times + 1):
        offset = str(i * 10)
        print(offset)
        data = session.get(getFollowing_url + offset, headers=ZHLogin.headers)
        source = json.loads(data.content.decode('utf-8'))
        for item in source['data']:
            print(item['url_token'])
            f.write(item['url_token'] + '\n')
    f.close()


def getFollowersInNewVersion(userID):
    followers_url = 'http://www.zhihu.com/people/' + userID + '/followers'
    fileName = userID + ".txt"
    f = open('Followers/' + fileName, 'w')
    response = session.get(followers_url, headers=ZHLogin.headers)
    soup = BeautifulSoup(response.content, 'lxml')
    total = soup.findAll(
        'div', {'class': 'Profile-followStatusValue'})[1].text
    # print(total)

    getFollowers_url = 'https://www.zhihu.com/api/v4/members/' + userID + \
        '/followers?per_page=10&include=data%5B%2A%5D.employments%2Ccover_url%2Callow_message%2Canswer_count%2Carticles_count%2Cfavorite_count%2Cfollower_count%2Cgender%2Cis_followed%2Cmessage_thread_token%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=10&offset='

    times = int(int(total) / 10)
    for i in range(1, times + 1):
        offset = str(i * 10)
        print(offset)
        data = session.get(getFollowers_url + offset, headers=ZHLogin.headers)
        source = json.loads(data.content.decode('utf-8'))
    # try:
    #     source = json.loads(str(data.content).split('\'')[1])
    # except:
    #     source = json.loads(str(data.content).split('\'')[
    #                         1].replace('\\', ''))
        for item in source['data']:
            print(item['url_token'])
            f.write(item['url_token'] + '\n')
    f.close()

    # data = session.get(getFollowers_url + '90', headers=ZHLogin.headers)
    # print(data.content.decode('utf-8'))
    # source = json.loads(data.content.decode('utf-8'))
    # source = json.loads(str(data.content).split('\'')[1])
    # for item in source['data']:
    #     print(item['url_token'])
    # f.write(item['url_token'] + '\n')


def getFollowersInOldVersion(userID):
    followers_url = 'https://www.zhihu.com/people/' + userID
    file_name = userID + '.txt'
    f = open('Followers/' + file_name, 'w')
    response = session.get(followers_url, headers=ZHLogin.headers)
    soup = BeautifulSoup(response.content, 'lxml')
    # total = soup.findAll(
    #     'div', {'class': {'zm-profile-side-section'}})
    print(soup)
    infolist = soup.find_all('a', {'class': 'item'})
    total = int(infolist[len(infolist) - 1].strong.string)


def saveUserInfotoDB(userInfo, dbName):
    db.dbName.insert({'name': userInfo.name, 'location': userInfo.location,
                      'gender': userInfo.gender, 'business': userInfo.business, 'education': userInfo.education,
                      'answers': userInfo.answers, 'asks': userInfo.asks, 'posts': userInfo.posts,
                      'collections': userInfo.collections, 'following': userInfo.following,
                      'followers': userInfo.followers, 'avatar_url': userInfo.avatar_url,
                      'agree': userInfo.agree, 'thanks': userInfo.thanks,
                      'logs': userInfo.logs, 'receive': userInfo.receive,
                      'bePosts': userInfo.bePosts, 'localAvatar': userInfo.localAvatar})


def getUserInfoInNewVersion(userID):
    user = Zhihuer.Zhihuer()
    response = session.get(user_url + userID +
                           '/followers', headers=ZHLogin.headers)
    # print(user_url + userID + '/followers')
    soup = BeautifulSoup(response.content, 'lxml')
    user.name = soup.find('span', {'class': 'ProfileHeader-name'}).text
    ProfileHeaderInfoItem = soup.find_all(
        'div', {'class': 'ProfileHeader-infoItem'})
    # print(ProfileHeaderInfoItem)
    for item in ProfileHeaderInfoItem:
        for it in item.find_all('div', {'class': 'ProfileHeader-iconWrapper'}):
            if it.find('svg').attrs['class'] == ['Icon', 'Icon--location']:
                user.location = item.text
            if it.find('svg').attrs['class'] == ['Icon', 'Icon--male']:
                user.gender = 'male'
            elif it.find('svg').attrs['class'] == ['Icon', 'Icon--female']:
                user.gender = 'female'
            elif it.find('svg').attrs['class'] == ['Icon', 'Icon--company']:
                user.business = item.text
            elif it.find('svg').attrs['class'] == ['Icon', 'Icon--education']:
                user.education = item.text
    ProfileSideColumnItem = soup.findAll(
        'div', {'class': 'Profile-sideColumnItem'})
    for item in ProfileSideColumnItem:
        if item.find('svg').attrs['class'] == ['Icon', 'IconGraf-icon', 'Icon--marked']:
            user.receive = item.text.split(' ')[1]
        elif item.find('svg').attrs['class'] == ['Icon', 'IconGraf-icon', 'Icon--like']:
            user.agree = item.text.split(' ')[1]
            if item.find('div', {'class': 'Profile-sideColumnItemValue'}).text != '':
                user.thanks = item.find(
                    'div', {'class': 'Profile-sideColumnItemValue'}).text.split('，')[0].split(' ')[1]
                if item.find('div', {'class': 'Profile-sideColumnItemValue'}).text.find('，') > 0:
                    user.bePosts = item.find(
                        'div', {'class': 'Profile-sideColumnItemValue'}).text.split('，')[1].split(' ')[0]
        elif item.find('svg').attrs['class'] == ['Icon', 'IconGraf-icon', 'Icon--commonEdit']:
            user.logs = item.text.split(' ')[1]
    ProfileMainTabs = soup.find_all('li', {'class': 'Tabs-item'})
    user.answers = ProfileMainTabs[1].find('span').text
    user.posts = ProfileMainTabs[2].find('span').text
    user.asks = ProfileMainTabs[3].find('span').text
    user.collections = ProfileMainTabs[4].find('span').text

    user.following = soup.findAll(
        'div', {'class': 'Profile-followStatusValue'})[0].text
    user.followers = soup.findAll(
        'div', {'class': 'Profile-followStatusValue'})[1].text
    user.avatar_url = soup.find('img', {'class': {'Avatar', 'Avatar--large',
                                                  'UserAvatar', 'ProfileHeader-avatar'}}).attrs['srcset'].split(' ')[0]
    urlretrieve(user.avatar_url, 'FollowingAvatar/' +
                user.name + '-' + userID + '.jpg')
    user.localAvatar = 'FollowingAvatar/' + user.name + '-' + userID + '.jpg'
    return user


def getUserInfoInOldVersion(userID):
    user = Zhihuer.Zhihuer()
    response = session.get(user_url + userID, headers=ZHLogin.headers)
    soup = BeautifulSoup(response.content, 'lxml')
    user.name = soup.find_all('span', {'class': 'name'})[0].text
    user.location = soup.find('span', {'class': 'location item'})
    if user.location is None:
        user.location = 'None'
    else:
        user.location = user.location.text
    user.business = soup.find('span', {'class': 'business item'})
    if user.business is None:
        user.business = 'None'
    else:
        user.business = user.business.text
    user.gender = soup.find('input', {'checked': 'checked'})
    if user.gender is None:
        user.gender = 'None'
    else:
        user.gender = user.gender['class'][0]
    user.employment = soup.find('span', {'class': 'employment item'})
    if user.employment is None:
        user.employment = 'None'
    else:
        user.employment = user.employment.text
    user.position = soup.find('span', {'class': 'position item'})
    if user.position is None:
        user.position = 'None'
    else:
        user.position = user.position.text
    user.education = soup.find('span', {'class': 'education item'})
    if user.education is None:
        user.education = 'None'
    else:
        user.education = user.education.text
    user.major = soup.find('span', {'class': 'education-extra item'})
    if user.major is None:
        user.major = 'None'
    else:
        user.major = user.major.text
    user.agree = int(
        soup.find('span', {'class': 'zm-profile-header-user-agree'}).strong.string)
    user.thanks = int(
        soup.find('span', {'class': 'zm-profile-header-user-thanks'}).strong.string)
    infolist = soup.find_all('a', {'class': 'item'})
    user.asks = int(infolist[1].span.text)
    user.answers = int(infolist[2].span.text)
    user.posts = int(infolist[3].span.text)
    user.collections = int(infolist[4].span.text)
    user.logs = int(infolist[5].span.text)
    user.following = int(infolist[len(infolist) - 2].strong.string)
    user.followers = int(infolist[len(infolist) - 1].strong.string)
    user.scantime = int(soup.find_all('span', {'class': 'zg-gray-normal'})[
        len(soup.find_all('span', {'class': 'zg-gray-normal'})) - 1].strong.string)
    user.avatar_url = soup.find(
        'img', {'class': {'Avatar', 'Avatar--is'}}).attrs['srcset'].split(' ')[0]
    urlretrieve(user.avatar_url, 'FollowingAvatar/' +
                user.name + '-' + userID + '.jpg')
    user.localAvatar = 'FollowingAvatar/' + user.name + '-' + userID + '.jpg'
    return user


# def main():

# chooseVersion('yang-yuan-83-58')
# getFollowersInNewVersion('yang-yuan-83-58')
# getUserInfoInNewVersion('excited-vczh')
# getFollowersInOldVersion('tian-yuan-dong')

# 关注者信息
# file = open('Followers/excited-vczh.txt', 'r')
# userlist = file.readlines()
# i = 0
# for user in userlist:
#     i += 1
#     if i < 2200:
#         continue
#     print(i)
#     chooseVersion(user.replace('\n', ''))

# 关注了的人信息
file = open('Following/excited-vczh.txt', 'r')
userlist = file.readlines()
i = 0
for user in userlist:
    i += 1
    if i < 1528:
        continue
    print(i)
    chooseVersion(user.replace('\n', ''), 'Following')
getFollowingInNewVersion('excited-vczh')
# chooseVersion('xi-lan-5-74')
