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

def UserByNum(users, num):
    for user in users:
        if (user.num == num):
            return user
    return None

def TweetsByUser(tweets, user):
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
            user = UserByNum(users, userNum)
        friendNum = (lines[i + 1])[0:-1]
        friend = UserByNum(users, friendNum)
        
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
            user = UserByNum(users, userNum)
        #날짜 무시
        if(user == None):
            print("Error: User not exitst (TweetFile) (" + userNum + ")");
            continue;
        word = (lines[i + 2])[0:-1]
        AddTweet(tweets, user, word)
        #print("Tweet added (" + userNum + ")") #디버깅용
    print("All tweets added")

##

def Statistics(users, tweets):
    totalFriendship = 0
    totalTweets = 0
    for user in users:
        totalFriendship += len(user.friends)
    for tweet in tweets:
        totalTweets += len(tweet.tweetedUsers)
    return (len(users), totalFriendship, totalTweets)

def Top5Words(tweets):
    tweets.sort(key=lambda tweet:len(tweet.tweetedUsers), reverse=True)
    return tweets[:5]

def Top5Users(users, tweets):
    users.sort(key=lambda user:len(TweetsByUser(tweets, user)), reverse=True)
    return users[:5]


def UsersTweetedWord(tweets, targetWord):
    resUsers = []
    for tweet in tweets:
        if(tweet.word == targetWord):
            resUsers = resUsers + tweet.tweetedUsers
    resUsers = list(set(resUsers))  #중복 제거
    return resUsers
    
def FriendsOfUsers(targetUsers):
    resUsers = []
    for targetUser in targetUsers:
        resUsers = resUsers + targetUser.friends
    resUsers = list(set(resUsers))  #중복 제거
    return resUsers

def DeleteTweetsByWord(tweets, targetWord):
    deletedUsers = []
    for tweet in tweets:
        if(tweet.word == targetWord):
            deletedUsers = deletedUsers + tweet.tweetedUsers
            tweets.remove(tweet)
    deletedUsers = list(set(deletedUsers))  #중복 제거
    return deletedUsers

def DeleteUser(users, targetUsers):
    for targetUser in targetUsers:
        users.remove(targetUser)

def printFinish():
    print("====Finished====")
    print()
            
def main():
    users = []
    tweets = []
    usersTweeted = None
    usersTweetsDeleted = None
    while (1):
        print("0. Read data files")
        print("1. Display statistics")
        print("2. Top 5 most tweeted words")
        print("3. Top 5 most tweeted users")
        print("4. Find users who tweeted a word")
        print("5. Find all people who are friends of the above users")
        print("6. Delete all mentions of a word")
        print("7. Delete all users who mentioned a word")
        print("8. Find strongly connected components")
        print("9. Find shortest path from a given user")
        print("99. Quit")
        print("Select Menu: ", end='')
        selectNum = int(input())
        if (selectNum == 0):
            print("====Read data files====")
            
            ReadUserFile(users, "user.txt")
            ReadFriendFile(users, "friend.txt")
            ReadTweetFile(tweets, users, "word.txt")

            printFinish()
        elif (selectNum == 1):
            print("====Display statistics====")

            result = Statistics(users, tweets)
            
            print("Total users:", result[0])
            print("Total friendship records:", result[1])
            print("Total tweets:", result[2])
            printFinish()
        elif (selectNum == 2):
            print("====Top 5 most tweeted words====")

            result = Top5Words(tweets)

            for resTweet in result:
                print(resTweet.word)
            printFinish()
        elif (selectNum == 3):
            print("====Top 5 most tweeted users====")

            result = Top5Users(users, tweets)

            for resUser in result:
                print(resUser.name)
            printFinish()
        elif (selectNum == 4):
            print("====Find users who tweeted a word====")
            print("Target word: ", end='')
            targetWord = input()

            usersTweeted = UsersTweetedWord(tweets, targetWord)

            for userTweeted in usersTweeted:
                print(userTweeted.name)
            printFinish()
        elif (selectNum == 5):
            print("====Find all people who are friends of the above users====")
            if(usersTweeted == None):
                print("Error: No target user. You must run menu no.4 first.")
                printFinish()
                continue
            else:
                result = FriendsOfUsers(usersTweeted)

                for resUser in result:
                    print(resUser.name)
                printFinish()
        elif (selectNum == 6):
            print("====Delete all mentions of a word====")
            print("Target word: ", end='')
            targetWord = input()

            usersTweetsDeleted = DeleteTweetsByWord(tweets, targetWord)

            printFinish()
        elif (selectNum == 7):
            print("====Delete all users who mentioned a word====")
            if(usersTweetsDeleted == None):
                print("Error: No target user. You must run menu no.6 first.")
                printFinish()
                continue
            else:
                DeleteUser(users, usersTweetsDeleted)
            printFinish()
        elif (selectNum == 99):
            print("bye.")
            break
        else:
            print("====Worng number====")
            print("Error: Please select from above menu.")
            print("====Finished====")
            print()
    
main()
