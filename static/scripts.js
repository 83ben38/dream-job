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
})