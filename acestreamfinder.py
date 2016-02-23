#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, re, praw
def get_stream(r, title_id):
    ace = re.compile('acestream:\/\/')

    submission = r.get_submission(submission_id=title_id)
    
    #Flatten comments
    comments = praw.helpers.flatten_tree(submission.comments)
    
    #Search through the comments until a link is found
    for comment in comments:
    
        #Use regex to find a match 
        m = re.search(ace, comment.body)
        
        #AceStream check 
        if m:
            print sys.argv[0], ": Found AceStream link!", m2.group(0)
            print sys.argv[0], ": Loading link"
            print(m2.group(0))
            sys.exit()
            
    sys.exit()

#Searches the requested subreddit for the title that has the users specified team    
def team_search(sub, team):
    post_limit = 25
    p = re.compile(team, re.IGNORECASE)
    
    # Connect to reddit and download the subreddit front page
    r = praw.Reddit(user_agent='Ace Sport Streams v1.0 by /u/a1ibs') 
    submissions = r.get_subreddit(sub).get_hot(limit=post_limit)
  
    #Process all the submissions from the specificed subreddit
    for submission in submissions:
        m = p.search(submission.title)
        
        #Once found call get_stream otherwise the program will keep looking and eventually quit
        if m:
            print sys.argv[0], ": Found it!", submission.title
            print sys.argv[0], ": Working on finding stream"
            get_stream(r, submission.id)
    print "Error: No thread found with that team, please try again"
    sys.exit()        
 
#Main function to check if the user entered the proper commands
def main():
    
    #Check for proper parameters
    if len(sys.argv) < 3:
        print 'Usage: python',sys.argv[0], '\'subreddit\' \'a\' \'team\''
        print 'Example1: python', sys.argv[0], 'soccerstreams Barcelona'
        print 'Example2: python', sys.argv[0], 'NHLStreams Calgary Flames'
        sys.exit()
    if len(sys.argv) == 3:
        team_search(sys.argv[1], sys.argv[2])
    else:
        team = sys.argv[2]
        team += ' '
        team += sys.argv[3]
        team_search(sys.argv[1], team)  
    

if __name__ == "__main__":
    main()
