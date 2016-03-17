#!flask/bin/python
from flask import Flask, jsonify, request
import re, praw, json

app = Flask(__name__)

@app.route('/sport')
def request_subreddit(): 

    #Handles the drop down menu for the sports
    asubreddit = request.args.get('subreddit')
    all_teams = find_teams(asubreddit)
    return json.dumps(all_teams)

@app.route('/')
def request_handler():
    
    #Receives the information from the user(Main function)
    asubreddit = request.args.get('subreddit')
    team1 = request.args.get('team')
    r, post_id = team_search(asubreddit, team1) 
    alink = get_stream(r, post_id)    
    return alink
   
def get_stream(r, title_id):
    check = 0
    #John Gruber's regex to find URLs in plain text, converted to Python/Unicode
    #See: http://daringfireball.net/2010/07/improved_regex_for_matching_urls  
    url = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
    
    ''' Not using these methods anymore, will just return the first url
    youtube = re.compile('(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?')
    ace = re.compile('acestream:\/\/[a-zA-Z0-9]+')
    '''    
    submission = r.get_submission(submission_id=title_id)
    
    #Flatten comments
    comments = praw.helpers.flatten_tree(submission.comments)
    
    
    for comment in comments:  
        #If a url is found ask the user if they would like to load it otherwise keep looking
        m2 = url.search(comment.body)
        if m2:
            return m2.group(0)
            #This might be implemented for later uses to work with the website
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
    
#This function will find all the teams based on the Thread: posts in the subreddit
def find_teams(sub):
    p = re.compile(ur'^(?:(?:Game)|(?:Match) Thread)(?:.*?)[:\]]\s?((?:[A-z]+\s)+)(?:(?:at)|(?:vs\.?)|(?:-))\s?((?:[A-z]+\s?)+)', re.IGNORECASE)
    post_limit = 25
    no_link = 1
    teams = []
    # Connect to reddit and download the subreddit front page
    r = praw.Reddit(user_agent='Sport Streams v2.5 by /u/a1ibs')
    post_limit = 25
    submissions = r.get_subreddit(sub).get_hot(limit=post_limit)
    
    #Finds all the submissions based on the 'Thread:'
    for submission in submissions:
        m = p.search(submission.title)
        if m:    
            no_link = 0
            #add the teams to the list of teams
            teams.append(m.group(1))
            teams.append(m.group(2))
    
    if no_link == 0:
        return teams
    else:
        return "0"
    
#Searches the requested subreddit for the title that has the users specified team    
def team_search(sub, team):

    # Connect to reddit and download the subreddit front page
    r = praw.Reddit(user_agent='Sport Streams v2.5 by /u/a1ibs')
    post_limit = 25
    p = re.compile(team, re.IGNORECASE)
    submissions = r.get_subreddit(sub).get_hot(limit=post_limit)
  
    #Process all the submissions from the specificed subreddit
    for submission in submissions:
        m = p.search(submission.title)
        
        #Once found call get_stream otherwise the program will keep looking and eventually quit
        if m:
            return r,submission.id

if __name__ == '__main__':
    app.run()
