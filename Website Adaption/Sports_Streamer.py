#!flask/bin/python
from flask import Flask, jsonify, request
import re, praw
import traceback

app = Flask(__name__)

@app.route('/')
def request_handler():
    #Receives the information from the user(Main function)
    
    subreddit = request.args.get('subreddit')
    team1 = request.args.get('team')
    the_type = request.args.get('type')
    
    # Connect to reddit and download the subreddit front page
    r = praw.Reddit(user_agent='Sport Streams v2.0 by /u/a1ibs')
    
    #Added these try and excepts to fix some pyopenssl errors
    try:
        post_id = team_search(r, subreddit, team1)  
    except Exception as ex:
        traceback.print_exc()
    try:
        alink = get_stream(r, post_id, the_type)
    except Exception as ex:
        traceback.print_exc()
        
    return alink
   
def get_stream(r, title_id, user_type):
    check = 0
    #John Gruber's regex to find URLs in plain text, converted to Python/Unicode
    #See: http://daringfireball.net/2010/07/improved_regex_for_matching_urls  
    url = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
    
    youtube = re.compile('(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?')
    
    ace = re.compile('acestream:\/\/[a-zA-Z0-9]+')
        
    submission = r.get_submission(submission_id=title_id)
    
    #Flatten comments
    comments = praw.helpers.flatten_tree(submission.comments)
    
    #Load proper regex
    if user_type == 'y':
        p2 = re.compile(youtube)
    elif user_type == 'u':
        p2 = re.compile(url)
    elif user_type == 'a':
        p2 = re.compile(ace)
    
    for comment in comments:  
        #If a url is found ask the user if they would like to load it otherwise keep looking
        m2 = p2.search(comment.body)
        if m2:
            return m2.group(0)
            
            #This will be implemented for later uses to work with the website
            '''
            check = 1
            print sys.argv[0], ": Found ", m.group(0)
            load = raw_input('Would you like to load this link?(y/n)')
            if load == 'y':
                print sys.argv[0], ": Loading link"
                webbrowser.open_new_tab(m.group(0))
                sys.exit()
           '''
    return "No Link Sorry"

#Searches the requested subreddit for the title that has the users specified team    
def team_search(r,sub, team):
    post_limit = 25
    p = re.compile(team, re.IGNORECASE) 
    submissions = r.get_subreddit(sub).get_hot(limit=post_limit)
  
    #Process all the submissions from the specificed subreddit
    for submission in submissions:
        m = p.search(submission.title)
        
        #Once found call get_stream otherwise the program will keep looking and eventually quit
        if m:
            return submission.id

if __name__ == '__main__':
    app.run()
