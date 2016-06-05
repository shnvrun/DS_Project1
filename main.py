class User:
    def __init__(self):
        self.num = '(none)'
        self.name = '(none)'
        self.friends = []

class Tweet:
    def __init__(self):
        self.word = '(none)'
        self.tweetedUsers = []


def AddTweet(tweets, user, word):
    for tweet in tweets:
        if (tweet.word == word):    #같은 단어를 가진 트윗이 존재하면
            tweet.tweetedUsers.append(user)
            return tweet
    #같은 단어의 트윗이 존재하지 않으면
    newTweet = Tweet()
    newTweet.word = word
    newTweet.tweetedUsers.append(user)
    tweets.append(newTweet)
    return newTweet

def userByNum(users, num):
    for user in users:
        if (user.num == num):
            return user
    return None

def ReadUserFile(users, filePath):
    file = open(filePath)
    lines = file.readlines()
    for i in range(0, len(lines), 4):
        newUser = User()
        newUser.num = (lines[i])[0:-1]   #개행 문자를 무시
        #날짜 무시
        newUser.name = (lines[i + 2])[0:-1]
        users.append(newUser)

        #디버깅용
        print("User added (" + newUser.num + ", " + newUser.name + ")")

def ReadFriendFile(users, filePath):
    file = open(filePath)
    lines = file.readlines()
    for i in range(0, len(lines), 3):
        userNum = (lines[i])[0:-1]
        friendNum = (lines[i + 1])[0:-1]
        user = userByNum(users, userNum)
        friend = userByNum(users, friendNum)
        
        if ((user == None) or (friend == None)):
            print("Error: User not exist (FriendFile) (" + userNum + ", " + friendNum + ")")
            continue;
        else:
            user.friends.append(friend);
            print("Friend added (" + userNum + ", " + friendNum + ")")
            
def ReadTweetFile(tweets, users, filePath):
    file = open(filePath)
    lines = file.readlines()
    for i in range(0, len(lines), 4):
        userNum = (lines[i])[0:-1]
        user = userByNum(users, userNum)
        #날짜 무시
        if(user == None):
            print("Error: User not exitst (TweetFile) (" + userNum + ")");
            continue;
        word = (lines[i + 2])[0:-1]
        AddTweet(tweets, user, word)
        print("Tweet added (" + userNum + ")")

def ReadDataFiles(users, tweets):
    ReadUserFile(users, "user.txt")
    ReadFriendFile(users, "friend.txt")
    ReadTweetFile(tweets, users, "word.txt")
            
def main():
    ReadDataFiles(users, tweets)
    
users = []
tweets = []
main()