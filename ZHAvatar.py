import ZHLogin
from bs4 import BeautifulSoup
import json
from urllib.request import urlretrieve
import Zhihuer

user_url = 'https://www.zhihu.com/people/'
session = ZHLogin.login()


def chooseVersion(userID):
    response = session.get(user_url + userID, headers=ZHLogin.headers)
    soup = BeautifulSoup(response.content, 'lxml')
    name = soup.find_all('span', {'class': 'name'})
    if name == []:
        pass
    else:
        getUserInfoInOldVersion(userID)


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
    user.receive = ProfileSideColumnItem[0].text.split(' ')[1]
    user.agree = ProfileSideColumnItem[1].text.split(' ')[1]
    user.thanks = ProfileSideColumnItem[1].find(
        'div', {'class': 'Profile-sideColumnItemValue'}).text.split('，')[0].split(' ')[1]
    user.bePosts = ProfileSideColumnItem[1].find(
        'div', {'class': 'Profile-sideColumnItemValue'}).text.split('，')[1].split(' ')[0]
    user.logs = ProfileSideColumnItem[2].text.split(' ')[1]
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
    urlretrieve(user.avatar_url, 'avatarPic/' +
                user.name + '-' + userID + '.jpg')


def getUserInfoInOldVersion(userID):
    user = Zhihuer.Zhihuer()
    response = session.get(user_url + userID, headers=ZHLogin.headers)
    soup = BeautifulSoup(response.content, 'lxml')
    user.name = soup.find_all('span', {'class': 'name'})[0].text
    user.location = soup.find('span', {'class': 'location item'})
    if user.location == None:
        user.location = 'None'
    else:
        user.location = user.location.text
    user.business = soup.find('span', {'class': 'business item'})
    if user.business == None:
        user.business = 'None'
    else:
        user.business = user.business.text
    user.gender = soup.find('input', {'checked': 'checked'})
    if user.gender == None:
        user.gender = 'None'
    else:
        user.gender = user.gender['class'][0]
    user.employment = soup.find('span', {'class': 'employment item'})
    if user.employment == None:
        user.employment = 'None'
    else:
        user.employment = user.employment.text
    user.position = soup.find('span', {'class': 'position item'})
    if user.position == None:
        user.position = 'None'
    else:
        user.position = user.position.text
    user.education = soup.find('span', {'class': 'education item'})
    if user.education == None:
        user.education = 'None'
    else:
        user.education = user.education.text
    user.major = soup.find('span', {'class': 'education-extra item'})
    if user.major == None:
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
    urlretrieve(user.avatar_url, 'avatarPic/' + name + '-' + userID + '.jpg')

# chooseVersion('chen-bin-77-56')
getUserInfoInNewVersion('excited-vczh')
