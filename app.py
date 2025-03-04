from flask import Flask, render_template, request
from openai import OpenAI
app = Flask(__name__)
data = open("key.txt",'r').read()
client = OpenAI(api_key=data)
# All of the webpages
def register_pages():
    @app.route('/')
    #Home page/aptitude test
    def index():
        return render_template('index.html')

    @app.route('/job')
    #Page for a single job
    def job():
        return render_template('job.html')

    @app.route('/jobs')
    #Page with a list of jobs 
    def jobs():
        return render_template('jobs.html')

    @app.route('/search')
    #Page to search for any job
    def search():
        return render_template('search.html')

#All of the methods for aptitude test
def register_aptitude_test():
    history = [{
        "role":"system",
        "content":"Create statements for an aptitude test which a user will rate from 1 to 7, 1 being strongly disagree, 4 being neutral, and 7 being strongly agree. Create one statement at a time starting with something like 'I like' or 'I am good at' or 'I prefer'. Make sure to cover multiple skill dimensions (hard skills, soft skills, and technical skills) After 15 statements, you may say only 'done' if you think you have a job to assign to them. You must say 'done' before 30 statements. Create the first statement."
    }]
    @app.route('/get_question',methods=['POST'])
    #Generates the next question for the aptitude test
    def get_question():
        if (len(history)==1):
            #Generate first question
            question = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
            ).choices[0].message.content.strip()
            #Add to history
            history.append({"role":"assistant",
                           "content":question})
            #Return
            return {"question":question,"done":False}
        #Add user rating to history
        history.append({"role":'user','content':str(request.json['rating'])})
        #Generate next question
        question = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
            ).choices[0].message.content.strip()
        #Add to history
        history.append({"role":"assistant",
                           "content":question})
        #If the bot is done
        if (len(question)<6):
            #Add prompt
            history.append({"role":"system",
                            "content":"Respond with only the job you assign to the user."})
            #Generate job choice
            job=client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
            ).choices[0].message.content.strip()
            #Return
            return {"done":True,"job_name":job}
        #Return
        return {"question":question,"done":False}

#All of the methods for job page
def register_job():

    @app.route('/generate_job_info', methods=['POST'])
    #Generates all of the info for a job page
    def generate_job_info():
        return {"error":"not implemented"}
    
    @app.route('/get_q_a',methods=['POST'])
    #responds to a q&a request
    def get_q_a():
        return {"error":'not implemented'}

if __name__ == '__main__':
    register_pages()
    register_aptitude_test()
    register_job()
    app.run(debug=False,host='127.0.0.1',port=3333)