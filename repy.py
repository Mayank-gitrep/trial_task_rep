# required libraries
import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

# initializing Flask
app = Flask(__name__)

# Home page
@app.route('/', methods=['GET', 'POST'])
def home():

    errors = []
    results = []
    
    if request.method == "POST":
        # get url that the person has entered
        try:
        	url = request.form['url']  # getting the url entered by user
        	r = requests.get(url)      # checking if the url works

	        if r:
	        	raw = BeautifulSoup(r.content, 'html.parser')  # getting a raw html data from web page
	        	# getting the required tags for 
	        	rp = raw.findAll('div',{'class':'grid--cell fs-title fc-dark'})  # reputation
	        	g = raw.findAll('div',{'class':'grid ai-center badge1-alternate'})  # gold
	        	s = raw.findAll('div',{'class':'grid ai-center badge2-alternate'})  # silver
	        	b = raw.findAll('div',{'class':'grid ai-center badge3-alternate'})  # bronze
	        	ans_ques_people = raw.findAll('div',{'class':'grid--cell fs-body3 fc-dark fw-bold'})  # answers, questions and people reached
	        	top = raw.findAll('span',{'class':'js-rank-badge grid--cell s-badge s-badge__votes fs-fine bc-blue-3 fc-blue-700'})  # overall ranking


	        	# computing the required
	        	repo = str(rp[0]).split('>')[1].split('<')[0]                 # reputation
	        	gold = str(g[0]).split('title="')[1].split(" ")[0]            # gold
	        	silver = str(s[0]).split('title="')[1].split(" ")[0]          # silver
	        	bronze = str(b[0]).split('title="')[1].split(" ")[0]          # bronze
	        	ans = str(ans_ques_people[0]).split('>')[1].split('<')[0]     # no. of answers
	        	ques = str(ans_ques_people[1]).split('>')[1].split('<')[0]    # no. of questions
	        	people = str(ans_ques_people[2]).split('>')[1].split('<')[0]  # People reached
	        	toprank = str(top[0]).split('_blank">')[1].split('</a>')[0].\
	        	replace('<b>','').replace('</b>','') + ' (based on Reputation)'  # rankings
	        	username = url.split('/')[-1]  # username

	        	# compiling everything into a list of tuples
	        	results = [('Username',username),('Reputation',repo),('Ranking',toprank),('Gold',gold),('Silver',silver),('Bronze',bronze),('Answers',ans),('Questions',ques),('People Reached',people)]

	        check = ans_ques_people[1]  # error check that everything above works
        except:
            errors.append("Unable to get URL. Please make sure it's valid and try again.")  # error if url is incorrect
            results = []  # making the result list to empty list
            return render_template('home.html', errors=errors)  # returning to webpage

    return render_template('home.html', errors=errors, results=results)  #returning to webpage


if __name__ == '__main__':
    app.run()