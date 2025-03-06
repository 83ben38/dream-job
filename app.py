from flask import Flask, render_template, request
from openai import OpenAI
import os
from langchain_community.utilities import WikipediaAPIWrapper
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
            "content":"Create statements for an aptitude test finding a dream job in one of the following categories: Science, Technology & Engineering, Math, Business & Economics, Healthcare, Education, Politics & Law, Art, Agriculture, Manufacturing & Construction, Entertainment, and Law Enforcement. A user will rate statements from 1 to 7, 1 being strongly disagree, 4 being neutral, and 7 being strongly agree. Create one statement at a time starting with something like 'I like' or 'I am good at' or 'I prefer' or 'I can'. Make sure to cover every job field with one statement. Make sure every statement only has one thing to rate. Do not include anything except the statement."}]

    @app.route('/get_question',methods=['POST'])
    #Generates the next question for the aptitude test
    def get_question():
        nonlocal history
        if not 'rating' in request.json:
            history = [{
            "role":"system",
            "content":"Create statements for an aptitude test finding a dream job in one of the following categories: Science, Technology & Engineering, Math, Business & Economics, Healthcare, Education, Politics & Law, Art, Agriculture, Manufacturing & Construction, Entertainment, and Law Enforcement. A user will rate statements from 1 to 7, 1 being strongly disagree, 4 being neutral, and 7 being strongly agree. Create one statement at a time starting with something like 'I like' or 'I am good at' or 'I prefer' or 'I can'. Make sure to cover every job field with one statement. Make sure every statement only has one thing to rate. Do not include anything except the statement."}]
            #Generate first question
            question = get_response()
            #Add to history
            history.append({"role":"assistant",
                           "content":question})
            #Return
            return {"question":question,"done":False}
        #Add user rating to history
        history.append({"role":'user','content':str(request.json['rating'])})
        if (len(history)==25):
            history.append({"role":"system",
                            "content":"Identify 1 to 3 categories in which the user might be interested in working in."})
            category = get_response()
            history.append({"role":"assistant","content":category})
            history.append({"role":"system","content":"Continue creating statements that help classify specific dream jobs within those categories. When you have a dream job for them, after 5 to 15 more questions, reply with only 'done' and nothing else."})
        #Generate next question
        question = get_response()
        #Add to history
        history.append({"role":"assistant",
                           "content":question})
        #If the bot is done
        if (len(question)<6):
            history.append({"role":"system","content":"Identify the category which is most suited for the user based on their prefrences."})
            category=get_response()
            history.append({"role":"assistant","content":category})
            #Add prompt
            history.append({"role":"system",
                            "content":"Respond with only the dream job you assign to the user in the identified field. Be extremely specific on what job they are assigned. Do not include any punctuation."})
            #Generate job choice
            job=get_response()
            #Return
            return {"done":True,"job_name":job}
        #Return
        return {"question":question,"done":False}

    #Returns AI Response
    def get_response():
        return client.chat.completions.create(
             model="gpt-4o-mini",
            messages=history,
        ).choices[0].message.content.strip()

#All of the methods for job page
def register_job():
    wi : WikipediaAPIWrapper
    @app.route('/generate_job_info', methods=['POST'])
    #Generates all of the info for a job page
    def generate_job_info(): 
        nonlocal wi
        wi = WikipediaAPIWrapper(top_k_results=1)
        job_name = request.json['job_name']
        data = wi.load(job_name)
        dict = {}
        dict["job_description"] = get_response("Generate a 3 paragraph description on what this job does: " +  job_name + " Wikipedia info related to the job: " + data[0].metadata['summary'])
        dict["skill_requirements"] = get_response("List 3 skill requirements for the following job, each on their own line: " + job_name + " Do not give anything except the requirements. Do not put numbers or dashes at the beginning of lines.").split("\n")
        dict["school_required"] = get_response("How much school is required for this job: " + job_name + "? Say only school requirements without explanations.")
        dict["salary"] = get_response("What is the range from 1st to 3rd quartile of pay on this job: " + job_name + "? Say only the money amounts with a dash between them.")
        image_options = [f for f in os.listdir("static/images")]
        dict["job_image"] = get_response("Pick an image that best represents the following job: " + job_name + ". You must pick an image, even if it is only loosely associated with the job. Images:" +str(image_options) + " Reply with only the image name and nothing else.")
        dict["similar_jobs"] = get_response("List 3 jobs similar to the following job, each on their own line: " + job_name + " Do not give anything except the jobs. Do not put numbers or dashes at the beginning of lines.").split("\n")
        dict["wiki_link"] = data[0].metadata['source']
        return dict
    

    #Returns an AI response
    def get_response(prompt):
        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages= [{"role":"system","content":prompt}]
        ).choices[0].message.content.strip()
    

    @app.route('/get_q_a',methods=['POST'])
    #responds to a q&a request
    def get_q_a():
        nonlocal wi
        data = wi.load(request.json['job_name'])
        return {"answer":get_response("Answer the following question: " + request.json['question'] + " using the following data: " + data[0].page_content + " If the data doesn't help answer the question, answer it to the best of your ability.")}

if __name__ == '__main__':
    register_pages()
    register_aptitude_test()
    register_job()
    app.run(debug=False,host='127.0.0.1',port=3333)