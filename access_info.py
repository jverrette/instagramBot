# We use requests to access information from other people's public instagram accounts
import requests # written with requests version 2.18.4
import sys
from bs4 import BeautifulSoup
import re

def insta_scrape(page, post = False):
    page = 'p/' + page if post else page
    wiki = 'https://www.instagram.com/'+page
    return requests.get(url=wiki)

# Get a list of successful dog Instagram accounts
def get_dog_accounts():
    wiki = 'https://www.thesprucepets.com/the-best-dog-instagrams-4165921'
    r = requests.get(url=wiki)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all(attrs={"data-type":"externalLink"})
    links = [link.get('href') for link in links if '/p/' not in link.get('href')]
    file = open('dog_accounts.txt', 'w')
    for link in links:
        file.write(link+'\n')
    file.close()
    return

def most_recent_submissions():
    arr = []
    file = open('dog_accounts.txt', 'r')
    for line in file:
        arr.append(line.strip())
    file.close()

    posts = []
    for account in arr:
        r = requests.get(url=account)
        post_ids = re.findall(r'(?<="shortcode":")[a-zA-Z0-9]+(?=")', r.text)
        posts.append(post_ids[0])

    file = open('recent_dog_posts.txt', 'w')
    for post in posts:
        file.write(post+'\n')
    file.close()
    return
    
def get_submissions():
    arr = []
    file = open('dog_accounts.txt', 'r')
    for line in file:
        arr.append(line.strip())
    file.close()

    posts = []
    for account in arr:
        r = requests.get(url=account)
        post_ids = re.findall(r'(?<="shortcode":")[a-zA-Z0-9]+(?=")', r.text)
        posts.extend(post_ids)

    file = open('dog_posts.txt', 'w')
    for post in posts:
        file.write(post+'\n')
    file.close()
    return
# We are looking to capture a list of posts.
# These show up in html as: "shortcode":"BupCOZkHa6l"
# The following returns a list of the strings for the post ids

'''
['BupCOZkHa6l',
 'BumSud9HsJq',
 'BukL6TrH7IO',
 'BujsbmpHdW8',
 'BujIec6nxNZ',
 'BuhUDDmn5iR',
 'BugzoKxHBwn',
 'Bue2GhVH6VU',
 'BuedE4eHdS0',
 'BuccsczHKqk',
 'BuZ6mygHK6n']
'''
#submission = 'BupCOZkHa6l'
def get_comments(submission):
    post_html = insta_scrape(submission, post = True)
    soup = BeautifulSoup(post_html.text, 'html.parser')
    # comments are within this script tag
    comments_all = soup.find(type="application/ld+json").contents[0]
    # The comments look like the following:
    # "text":"@krelingzabaleta the best idea!! So it will be a farm that doesn't grow anything, only adopts dogs \ud83d\ude02",
    return re.findall(r'(?<="Comment","text":")[^"]+(?=","author")', comments_all)
# rows 0-37 completed
# rows 51 through 103 completed
def create_comments_file(last_completed_post=0):
    # Get posts from saved file
    all_posts = []
    file = open('dog_posts.txt', 'r')
    for line in file:
        all_posts.append(line.strip())
    file.close()

    # Write comments to a file
    for num_posts_completed in range(len(all_posts)):
        if num_posts_completed < last_completed_post:
            continue
        try:
            comments = get_comments(all_posts[num_posts_completed])
            with open("dog_comments.txt", "a") as file:
                for comment in comments:
                    file.write(comment+'\n')

            print('%d of %d posts completed'%(num_posts_completed + 1, len(all_posts)))
        except:
            print('post %d of %d did not work!'%(num_posts_completed + 1, len(all_posts)))
            continue
    file.close()

def main():
    get_dog_accounts()
    get_submissions()
    create_comments_file()
    return
