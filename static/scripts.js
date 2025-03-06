document.addEventListener('DOMContentLoaded',function(){
    const page = window.location.pathname;
    if (page == '/'){
        fetch('/get_question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: 'none'})
        })
        .then(response => response.json())
        .then(data => {
            const question = document.getElementById('statement');
            question.textContent = data.question;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    if (page == '/job'){
        const params = new URLSearchParams(window.location.search);
        const job_name = params.get('job_name');
        document.title = 'Dream Jobs - '+job_name;
        const job_title = document.getElementById('job-title');
        job_title.textContent = job_name;
        fetch('/generate_job_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({job_name : job_name})
        })
        .then(response => response.json())
        .then(data => {
            const job_description = document.getElementById('job-description');
            job_description.textContent = data.job_description;
            const skill_requirements = document.getElementById('skill-requirements');
            for (item in data.skill_requirements){
                const li = document.createElement('li');
                li.textContent = data.skill_requirements[item];
                skill_requirements.appendChild(li);
            }
            const school_required = document.getElementById('school-required');
            school_required.textContent = data.school_required;
            const salary = document.getElementById('salary');
            salary.textContent = data.salary;
            const job_image = document.getElementById('job-image');
            job_image.src = "static/images/"+data.job_image;
            const similar_jobs = document.getElementById('similar-jobs');
            for (item in data.similar_jobs){
                const li = document.createElement('li')
                const a = document.createElement('a');
                a.textContent = data.similar_jobs[item];
                a.href = `job?job_name=${encodeURIComponent(data.similar_jobs[item])}`;
                li.appendChild(a);
                similar_jobs.appendChild(li);
            }
            const wiki_link = document.getElementById('wikipedia-link');
            wiki_link.href = data.wiki_link;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    var loading = false;
    window.response = function(rating){
        if (!loading){
            loading = true;
            const question = document.getElementById('statement');
            question.textContent = '...';
            fetch('/get_question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({rating : rating})
            })
            .then(response => response.json())
            .then(data => {
                if (data.done){
                    window.location.href = `job?job_name=${encodeURIComponent(data.job_name)}`;
                }
                else{
                    question.textContent = data.question;
                }
                loading = false;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }
    document.getElementById("qa-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the default form submission (page refresh)
        window.submit();
      });
    window.submit = function(){
        const params = new URLSearchParams(window.location.search);
        const job_name = params.get('job_name');
        const answerDiv = document.getElementById("qa-answers");
        const newDiv = document.createElement("div");
        const question = document.createElement("h3");
        newDiv.appendChild(question);
        answerDiv.appendChild(newDiv);
        const textField = document.getElementById("question");
        question.textContent = textField.value;
        textField.value = "";
        fetch('/get_q_a', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question.textContent, job_name: job_name})
        })
        .then(response => response.json())
        .then(data => {
            const answer = document.createElement("p");
            newDiv.appendChild(answer);
            answer.textContent = data.answer;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
})