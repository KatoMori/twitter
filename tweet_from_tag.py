"""
written by KatoMori
TILL_DAY-dayまで、keywordのtweet単体(RTなし)を取得
月跨ぎ,年跨ぎ未対応(そのうちなんとか)
"""
import tweepy
import setting
from time import sleep

# twitter keys
CONSUMER_KEY = setting.CONSUMER_KEY
CONSUMER_SECRET = setting.CONSUMER_SECRET
ACCESS_TOKEN = setting.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = setting.ACCESS_TOKEN_SECRET

# APIインスタンスを作成
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def analyze_tweet_tag_to_plt(tweets,TILL_DAY):
    tweet_count= 0
    flag = 0
    tag_list = []
    dict = read_tags_count(TARGET_TAG_PATH)
    searched_day = 100000
    TILL_DATE,TILL_TIME = divide_date(TILL_DAY)
    for tweet in tweets:
        print("------------------------------------------------")
        sesearched_day = reshape_day(str(tweet.created_at))
        date,time = divide_date(sesearched_day)
        ssearched_day_jst = to_jap_time(date,time)
        DATE,TIME = divide_date(ssearched_day_jst)
        print(tweet.entities)
        try:
            id = tweet.entities['user_mentions']
            print("id")
            if len(id) == 0:
                print("a")
                if compare_time(DATE, TILL_DATE): #曜日比較
                    print("b")
                    if compare_time(TIME, TILL_TIME):
                        print("c")
                        tweets_tags = tweet.entities['hashtags']
                        #print(range(len(tweet.entities['hashtags'])))
                        for num in range(len(tweet.entities['hashtags'])):
                            tag_name = tweets_tags[num]["text"]
                            tag_list.append(tag_name+':'+ssearched_day_jst)
                        tweet_count = tweet_count + 1
                        searched_day = tweet.created_at
        except:
            continue
    if searched_day == 100000:
        searched_day = sesearched_day
        flag = 1
    searched_day = reshape_day(str(searched_day))
    day,time = divide_date(searched_day)
    searched_day = to_jap_time(day,time)
    print("tag_list")
    print(tag_list)
    print("date comparison(back to the past)")
    print("{} --> {}".format(searched_day, TILL_DAY))
    return tag_list,searched_day,tweet_count,flag


# TILLのほうが小さい
def compare_time(TIME,TILL_TIME):
    for num in range(len(TIME)):
        if TIME[0] < TILL_TIME[0]: # year or hour
            return False
        elif TIME[1] < TILL_TIME[1]: # month or min
            return False
        elif TIME[2] < TILL_TIME[2]: # day or m_min
            return False
    return True


def note_tags(tag_list,TARGET_TAG_PATH):
    for content in tag_list:
        f = open(TARGET_TAG_PATH, 'a')  # overwrite
        f.write(content + '\n')
        f.close()


def read_tags_count(TXT_PATH):
    list = read_url(TXT_PATH)
    dict = {}
    for content in list:
        tag = content.split(':')
        dict[tag[0]] = tag[1]
    return dict


# read  used urls
def read_url(TXT_PATH):
    f = open(TXT_PATH)
    url_list = f.readlines() # f.readlines()でlistで返す
    for i in range(len(url_list)):
        url = url_list[i].split('\n')
        url_list[i] = url[0]
    f.close()
    return url_list


def interval():
    print("sleep start")
    print("[",end="")
    for i in range(15):
        sleep(60)
        if (i+1) % 5 != 0:
            print("{}".format("-"),end="")
        elif (i+1) % 5 == 0:
            print("{}".format("|"),end="")
    print("]")
    print("sleep out")


def divide_date(date):
    date = str(date)
    date = date.split('_')
    time = date[1].split(':')
    date = date[0].split('-')
    return date,time


# 月・年またぎ未対応てへぺろ
def to_jap_time(date,time):
    eng_day = date[0]+'-'+date[1]+'-'+date[2]+'_'+time[0]+':'+time[1]+':'+time[2]+'_ENG'
    print("eng_day ->jap day")
    print(eng_day+'->', end=' ')
    hour = int(time[0])
    day = int(date[2])
    hour = hour + 9
    if hour >= 24:
        hour = hour - 24
        if hour < 10:
            hour = '0' + str(hour)
        day = day + 1
    hour = str(hour)
    day = str(day)
    day = date[0]+'-'+date[1]+'-'+day+'_'+hour+':'+time[1]+':'+time[2]+'_JST'
    print(day)
    return day


# tweet.created_atを矯正してやる
def reshape_day(day):
    date = day.split(' ')
    date = date[0] + '_' + date[1] + '_JST'
    return date


# 検索キーワード
TARGET = 'snack'
TILL_DAY = "2020-09-20_18:00:00_JST"

# 保存先
PATH_DIR = './data/'
TARGET_DIR = TARGET + '/'
IMAGE_DIR = 'images/'
TARGET_PATH = PATH_DIR+TARGET_DIR
TARGET_IMAGE_PATH = TARGET_PATH+IMAGE_DIR
TARGET_TAG_PATH = TARGET_PATH+TARGET+'_tag_count.txt'


# search
if __name__ == '__main__':
    keywords = ["#スナック希世乃"]
    list = []
    for keyword in keywords:
        day = "2020-09-20_18:40:14_JST"  # 21
        first_day = day
        while (True):
            print("start day")
            print(day)
            print(keyword)
            tweets = api.search(q=keyword, count=100, until=day)  # 2020-09-21-00:00:00
            print("hit tweets:", end="")
            print(len(tweets))
            if len(tweets) == 0:
                break
            print("-----------")
            tag_list, day, tweet_count, flag = analyze_tweet_tag_to_plt(tweets, TILL_DAY)
            note_tags(tag_list, TARGET_TAG_PATH)
            print("tweets:", end="")
            print(tweet_count)
            if flag == 0 and tweet_count == 0:
                break
            interval()
    print("first day")
    print(first_day)

"""
# for error avoidance
        text = text.encode('cp932', 'ignore')
        text = text.decode('cp932')
"""

