#!flask/bin/python
from flask import Flask, jsonify
import re, praw

app = Flask(__name__)

@app.route('/')
def request_handler():
    #Receives the information from the user(Main function)
    # Connect to reddit and download the subreddit front page
    r = praw.Reddit(user_agent='Sport Streams v1.3 by /u/a1ibs')
    post_id = team_search(r, 'all', 'leo')
    link = get_stream(r, post_id)
    return link
    
def get_stream(r, title_id):

    check = 0
    
    #John Gruber's regex to find URLs in plain text, converted to Python/Unicode
    #See: http://daringfireball.net/2010/07/improved_regex_for_matching_urls  
    url = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
    
    youtube = re.compile('(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?')
    
    ace = re.compile('acestream:\/\/[a-zA-Z0-9]+')
    
    #Give the user a choice of streams
    user_type = 'y' 
    #raw_input('What kind of stream would you like (youtube/url/acestream)?(y/u/a)')
        
    submission = r.get_submission(submission_id=title_id)
    
    #Flatten comments
    comments = praw.helpers.flatten_tree(submission.comments)
    
    #Load proper regex
    if user_type == 'y':
        link = youtube
    elif user_type == 'u':
        link = url
    elif user_type == 'a':
        link = ace
        
    for comment in comments:  
        
        #If a url is found ask the user if they would like to load it otherwise keep looking
        m = re.search(link, comment.body)
        if m:
            #return the link found
            return m.group(0)
            '''
            check = 1
            print sys.argv[0], ": Found ", m.group(0)
            load = raw_input('Would you like to load this link?(y/n)')
            if load == 'y':
                print sys.argv[0], ": Loading link"
                webbrowser.open_new_tab(m.group(0))
                sys.exit()
           
            else:
                print sys.argv[0], ": Ok still looking"
             '''
    #sys.exit()

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
            #print sys.argv[0], ": Found it!", submission.title
            #print sys.argv[0], ": Working on finding stream"
            #return reddit object and the submission id
            return submission.id
    #print "Error: No thread found with that team, please try again"
    #sys.exit()        
 
   

if __name__ == '__main__':
    app.run()
