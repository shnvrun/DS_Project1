INF = 1E10

class User:
    def __init__(self):
        self.num = '(none)'
        self.name = '(none)'
        self.friends = []
        self.p = None
        self.d = None
        self.f = None
        self.color = "WHITE"

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

def DFSVisit(user, time):
    time = time + 1
    user.d = time
    user.color = "GRAY"     #enum으로 바꾸고싶다
    for friend in user.friends:
        if (friend.color == "WHITE"):
            friend.p = user
            time = DFSVisit(friend, time)
    user.color = "BLACK"
    time = time + 1
    user.f = time
    return time

def DFS(users):
    for user in users:
        user.color = "WHITE"
        user.p = None
    time = 0
    for user in users:
        if (user.color == "WHITE"):
            time = DFSVisit(user, time)

def Transpose(users):
    resUsers = []
    for user in users:
        userCopy = User()
        userCopy.num = user.num
        userCopy.name = user.name
        resUsers.append(userCopy)
    for user in users:
        for friend in user.friends:
            UserByNum(resUsers, friend.num).friends.append(UserByNum(resUsers, user.num))
    return resUsers

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

def DeleteUser(users, tweets, targetUsers):
    tUsers = Transpose(users)
    for targetUser in targetUsers:
        users.remove(targetUser)
        for tFriend in UserByNum(tUsers, targetUser.num).friends:
            UserByNum(users, tFriend.num).friends.remove(targetUser)
        for tweet in TweetsByUser(tweets, targetUser):
            tweet.tweetedUsers.remove(targetUser)
            if (len(tweet.tweetedUsers) <= 0):
                tweets.remove(tweet)

def FindSCC(users):
    DFS(users)
    users.sort(key=lambda user:user.f, reverse=True)
    tUsers = Transpose(users)
    DFS(tUsers)

    tUsers.sort(key=lambda user:user.f, reverse=True)

    '''
    for i, user in enumerate(users):
        print(user.name, user.d, user.f)
        if (i > 5):
            break
    print()
    for i, user in enumerate(tUsers):
        print(user.name, user.d, user.f)
        if (i > 5):
            break
    '''
    
    scc = []
    i = 0
    while (i < len(tUsers)):
        sccLen = ((tUsers[i].f - tUsers[i].d) + 1) // 2
        scc.append(tUsers[i:(i + sccLen)])
        i = i + sccLen
    return scc

def InitInf(targetUser, q):
    targetUser.color = "GRAY"
    for friend in targetUser.friends:
        if (friend.color != "GRAY"): #White로 초기화 과정이 없었으므로
            InitInf(friend, q)
    targetUser.d = INF
    q.append(targetUser)

def FindShortestPath(targetUser):
    s = []
    q = []
    InitInf(targetUser, q)
    targetUser.d = 0

    while (len(q) > 0):
        q.sort(key = lambda user:user.d)
        u = q[0]
        q.remove(u)
        s.append(u)
        for v in u.friends:
            if (u.d + len(v.friends) < v.d):    #현재 경로가 기존 경로의 weight보다 작으면
                v.d = u.d + len(v.friends)
                v.p = u
    return s
    
def PrintFinish():
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

            PrintFinish()
        elif (selectNum == 1):
            print("====Display statistics====")

            result = Statistics(users, tweets)
            
            print("Total users:", result[0])
            print("Total friendship records:", result[1])
            print("Total tweets:", result[2])
            PrintFinish()
        elif (selectNum == 2):
            print("====Top 5 most tweeted words====")

            result = Top5Words(tweets)

            for resTweet in result:
                print(resTweet.word)
            PrintFinish()
        elif (selectNum == 3):
            print("====Top 5 most tweeted users====")

            result = Top5Users(users, tweets)

            for resUser in result:
                print(resUser.name)
            PrintFinish()
        elif (selectNum == 4):
            print("====Find users who tweeted a word====")
            print("Target word: ", end='')
            targetWord = input()

            usersTweeted = UsersTweetedWord(tweets, targetWord)

            for userTweeted in usersTweeted:
                print(userTweeted.name)
            PrintFinish()
        elif (selectNum == 5):
            print("====Find all people who are friends of the above users====")
            if(usersTweeted == None):
                print("Error: No target user. You must run menu no.4 first.")
                PrintFinish()
                continue
            else:
                result = FriendsOfUsers(usersTweeted)

                for resUser in result:
                    print(resUser.name)
                PrintFinish()
        elif (selectNum == 6):
            print("====Delete all mentions of a word====")
            print("Target word: ", end='')
            targetWord = input()

            usersTweetsDeleted = DeleteTweetsByWord(tweets, targetWord)

            PrintFinish()
        elif (selectNum == 7):
            print("====Delete all users who mentioned a word====")
            
            if(usersTweetsDeleted == None):
                print("Error: No target user. You must run menu no.6 first.")
                PrintFinish()
                continue
            else:
                DeleteUser(users, tweets, usersTweetsDeleted)
                
            PrintFinish()
        elif (selectNum == 8):
            print("====Find strongly connected components====")

            scc = FindSCC(users)

            for sccUsers in scc:
                for user in sccUsers:
                    print(user.name, end='\t')
                print()
            PrintFinish()
        elif (selectNum == 9):
            print("====Find shortest path from a given user====")
            print("Target user (number): ", end='')
            targetUser = UserByNum(users, input())

            result = FindShortestPath(targetUser)
            result.remove(targetUser)
            result.sort(key = lambda user:user.d)
            result = result[0:5]

            print("Top 5")
            for user in result:
                print("D:", user.d, end='\t')
                while (user.p != None):
                    print(user.num, user.name, sep='/', end="\t<-- ")
                    user = user.p
                print(user.num, user.name, sep='/')
            PrintFinish()
        elif (selectNum == 99):
            print("bye.")
            break
        else:
            print("====Worng number====")
            print("Error: Please select from above menu.")
            print("====Finished====")
            print()
    
main()
