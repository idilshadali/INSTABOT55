import requests, urllib  #it opens url
from textblob import TextBlob #liberary of text data and provides API
from textblob.sentiments import NaiveBayesAnalyzer
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt

app_access_token = '1554854863.0748575.f695d53f0f9040d59a03e164cc1445e0' #access for instabot

BASE_URL = 'https://api.instagram.com/v1/' #api link


def my_info(): #it provides  user (self) info.
    permission_url = (BASE_URL + 'users/self/?access_token=%s') % (app_access_token)
    print 'GET request url : %s' % (permission_url) # it gets permission
    my_info = requests.get(permission_url).json()
    if my_info['meta']['code'] == 200:
        if len(my_info['data']):
            print 'Username: %s' % (my_info['data']['username'])
            print 'Number of people who are follow you.: %s' % (my_info['data']['counts']['followed_by'])
            print 'Number of people you follow.: %s' % (my_info['data']['counts']['follows'])
            print 'Number of posts.: %s' % (my_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 receive'


def fetch_sendbox_id(insta_username): #to get info of other user.
    permission_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, app_access_token)
    print 'GET request url : %s' % (permission_url)
    sendbox_info = requests.get(permission_url).json()

    if sendbox_info['meta']['code'] == 200:
        if len(sendbox_info['data']):
            return sendbox_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


def fetch_sendbox_info(insta_username): #it gives info of other user (sendbox)
    user_id = fetch_sendbox_id(insta_username)
    if user_id == None:
        print 'There is no user of this username.!'
        exit()
    permission_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, app_access_token)
    print 'GET request url : %s' % (permission_url)
    user_info = requests.get(permission_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Your Username is: %s' % (user_info['data']['username'])
            print 'No of followers you have: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


def fetch_my_post(): #it give user (self) post.
    permission_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (app_access_token)
    print 'GET request url : %s' % (permission_url)
    my_media = requests.get(permission_url).json()

    if my_media['meta']['code'] == 200:
        if len(my_media['data']):
            image_name = my_media['data'][0]['id'] + '.jpeg'
            image_url = my_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def fetch_sendbox_post(insta_username): #it gives sendbox user post
    user_id = fetch_sendbox_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    permission_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, app_access_token)
    print 'GET request url : %s' % (permission_url)
    sendbox_media = requests.get(permission_url).json()

    if sendbox_media['meta']['code'] == 200:
        if len(sendbox_media['data']):
            image_name = sendbox_media['data'][0]['id'] + '.jpeg'
            image_url = sendbox_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def fetch_post_id(username): #it gives sendbox user id
    user_id = fetch_sendbox_id(username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    permission_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, app_access_token)
    print 'GET request url : %s' % (permission_url)
    user_media = requests.get(permission_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


def like_a_post(insta_username): #it likes users post.
    media_id = fetch_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": app_access_token}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'You have successfully liked the post!'
    else:
        print 'Your like is unsuccessful. Try again!'


def post_a_comment(insta_username): #it is used for make comment on sendbox user
    media_id = fetch_post_id(insta_username)
    comment_text = raw_input("Write what you wants comment.: ")
    payload = {"access_token": app_access_token, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "You have successfully added a new comment on the post.!"
    else:
        print "Your comment is not posted. Try again!"


def delete_negative_comment(sendbox_username):  #it deletes the negative comments from the users post.
    media_id = fetch_post_id(sendbox_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, app_access_token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, app_access_token)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'Comments on found on the post!'
    else:
        print 'Status code other than 200 received!'


def comparision_piechart(username):##function declaration to show number of positive and negative comments and plot a pie-chart
    media_id = fetch_post_id(username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, app_access_token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)



            for y in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][y]['id']
                comment_text = comment_info['data'][y]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg < blob.sentiment.p_pos):
                    print 'positive comment : %s' % (comment_text)
                    a = y + 1  # positive comments
                    b = x - y  # negative comments
                    print "No. of Positive comments: %s" % (a)
                    print "No. of negative comments: %s" % (b)
                    c = a + b
                    print "Total no. of comments: %s" %(c)
                    # Data to plot


                    labels = 'red', 'blue'
                    sizes = [a, b]
                    colors = ['red','blue']
                    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1%%', shadow=True, startangle=140)
                    plt.axis('equal')
                    plt.show()



        else:
            print 'Comments not found on the post!'
    else:
        print 'Status code other than 200 received!'




def start_bot(): #choise to give commend.
    while True:
        print '\n'
        print 'Welcome to InstaBot!'
        print 'These are some options you can with the help of InstaBot .:'
        print "1 You can fetch your own details."
        print "2 Fetch  details of sandbox user."
        print "3 Fetch your own post."
        print "4 Fetch the post of sendbox user."
        print "5 Like the recent post of the user."
        print "6 Make a comment on the post of sendbox user."
        print "7 Delete negative comments from the post of sandbox user."
        print "8 Plote pychart of posative and negative comments and show comment list"

        print "9 Exit."

        option = raw_input("Chosse you choice.:")
        if option == "1":
            my_info()
        elif option == "2":
            insta_username = raw_input("Enter username of user.: ")
            fetch_sendbox_info(insta_username)
        elif option == "3":
            fetch_my_post()
        elif option == "4":
            insta_username = raw_input("Enter username of user.: ")
            fetch_sendbox_post(insta_username)
        elif option == "5":
            insta_username = raw_input("Enter username of user.: ")
            like_a_post(insta_username)
        elif option == "6":
            insta_username = raw_input("Enter username of user.: ")
            post_a_comment(insta_username)
        elif option == "7":
            insta_username = raw_input("Enter username of user.: ")
            delete_negative_comment(insta_username)
        elif option == "8":
            username = raw_input("Enter username of user.")
            comparision_piechart(username)
        elif option == "9":
            exit()
        else:
            print "wrong input!\nTry Again"


start_bot()