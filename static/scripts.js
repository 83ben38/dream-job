document.addEventListener('DOMContentLoaded',function(){
    const page = window.location.pathname;
    if (page == '/index.html' || page == '/'){
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
    window.response = function(rating){
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
                const question = document.getElementById('statement');
                question.textContent = data.question;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
})