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

def tweetsByUser(tweets, user):
    result = []
    for tweet in tweets:
        if (tweet.tweetedUsers.count(user) > 0): #트윗한 사람중 유저가 존재하면
            result.append(tweet)
    return result

def ReadUserFile(users, filePath):
    print("Adding users...")
    file = open(filePath)
    lines = file.readlines()
    for i in range(0, len(lines), 4):
        newUser = User()
        newUser.num = (lines[i])[0:-1]   #개행 문자를 무시
        #날짜 무시
        newUser.name = (lines[i + 2])[0:-1]
        users.append(newUser)

        #디버깅용
        #print("User added (" + newUser.num + ", " + newUser.name + ")")
    print("All users added.")

def ReadFriendFile(users, filePath):
    print("Adding friends...")
    userNum = '(none)'
    
    file = open(filePath)
    lines = file.readlines()
    for i in range(0, len(lines), 3):
        if (userNum != (lines[i])[0:-1]):   #유저 번호가 이전과 다르면
            userNum = (lines[i])[0:-1]
            user = userByNum(users, userNum)
        friendNum = (lines[i + 1])[0:-1]
        friend = userByNum(users, friendNum)
        
        if ((user == None) or (friend == None)):
            print("Error: User not exist (FriendFile) (" + userNum + ", " + friendNum + ")")
            continue;
        else:
            user.friends.append(friend);
            #print("Friend added (" + userNum + ", " + friendNum + ")") #디버깅용
    print("All friends added")
            
def ReadTweetFile(tweets, users, filePath):
    print("Adding tweets...")
    userNum = '(none)'
    
    file = open(filePath)
    lines = file.readlines()
    for i in range(0, len(lines), 4):
        if (userNum != (lines[i])[0:-1]):   #유저 번호가 이전과 다르면
            userNum = (lines[i])[0:-1]
            user = userByNum(users, userNum)
        #날짜 무시
        if(user == None):
            print("Error: User not exitst (TweetFile) (" + userNum + ")");
            continue;
        word = (lines[i + 2])[0:-1]
        AddTweet(tweets, user, word)
        #print("Tweet added (" + userNum + ")") #디버깅용
    print("All tweets added")

def ReadDataFiles(users, tweets):
    ReadUserFile(users, "user.txt")
    ReadFriendFile(users, "friend.txt")
    ReadTweetFile(tweets, users, "word.txt")

def DisplayStatistics(users, tweets):
    totalFriendship = 0
    totalTweets = 0
    
    for user in users:
        totalFriendship += len(user.friends)
    for tweet in tweets:
        totalTweets += len(tweet.tweetedUsers)
        
    print("Total users:", len(users))
    print("Total friendship records:", totalFriendship)
    print("Total tweets:", totalTweets)

def Top5Words(tweets):
    tweets.sort(key=lambda tweet:len(tweet.tweetedUsers), reverse=True)
    for i in range(0, 5):
        print(tweets[i].word)

def Top5Users(users, tweets):
    users.sort(key=lambda user:len(tweetsByUser(tweets, user)), reverse=True)
    for i in range(0, 5):
        print(users[i].name)
            
def main():
    ReadDataFiles(users, tweets)
    DisplayStatistics(users, tweets)
    Top5Words(tweets)
    Top5Users(users, tweets)
    
users = []
tweets = []
main()
