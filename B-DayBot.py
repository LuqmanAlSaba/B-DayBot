import praw
import datetime
import random

REPLY_MESSAGES = ["Happy cake day /u/{}! 🍰",
                  "Hope you have a nice cake day /u/{}! 🎂",
                  "It's your cake day /u/{}! Congrats! 🎉",
                  "Happy Reddit birthday /u/{}! 🙂",
                  "Happy cake day /u/{}! [Here's some cake!](http://gph.is/1WDTNoY)"]


def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit("B-DayBot", user_agent="Birthday Bot v1.0 (by /u/LukeAlSaba)")
    return reddit


def main():
    reddit = authenticate()
    congratulated_users = get_congratulated_users()

    remove_downvoted_comments(reddit)
    run_bot(reddit, congratulated_users)


def run_bot(reddit, congratulated_users):
    current_date = datetime.datetime.today().strftime('%m/%d')

    print("Getting comments...")
    for comment in reddit.subreddit("WholesomeMemes+MadeMeSmile+RandomKindness").comments(limit=100):

        user_birthday = datetime.datetime.fromtimestamp(int(comment.author.created)).strftime('%m/%d')

        print("Checking...")
        if current_date == user_birthday and comment.author not in congratulated_users:
            print("Cake day found!")
            # comment.reply(random.choice(REPLY_MESSAGES).format(comment.author)).clear_vote()
            #
            # congratulated_users.append(comment.author)
            # with open("congratulated_users.txt", "a") as file:
            #     file.write("{}\n".format(comment.author.name))


def get_congratulated_users():
    with open("congratulated_users.txt", "r") as file:
        return file.read().split("\n")


def remove_downvoted_comments(reddit):
    print("Checking for comments with negative karma")
    for comment in reddit.redditor("B-DayBot").comments.new(limit=None):
        print("Comment Score: {}".format(comment.score))
        if comment.score < 0:
            print("Deleting comment...")
            comment.delete()


if __name__ == "__main__":
    main()
