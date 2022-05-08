let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')

let token = localStorage.getItem('token')

if(token){
    loginBtn.remove()
}else{
    logoutBtn.remove()
}

logoutBtn.addEventListener('click',(e)=>{
    e.preventDefault()
    localStorage.removeItem('token')
    window.location = 'http://127.0.0.1:5500/login.html'
})


let projectURL = 'http://127.0.0.1:8000/api/project/'
let getProject = () => {
    fetch(projectURL)
        .then(response => response.json())
        .then((data) => {
            buildProjects(data)
        })
}

let buildProjects = (projects) => {
    let projectsWrapper = document.getElementById('projects-wrapper')
    projectsWrapper.innerHTML = ''
    for (let i = 0; i < projects.length; i++) {
        let project = projects[i]
        let projectCard = `
        <div class="project--card">
            <img src="http://127.0.0.1:8000${project.featured_image}" alt="">

            <div>
                <div class="card--header">
                    <h3>${project.title}</h3>
                    <strong class="vote--option" data-vote="up" data-project="${project.id}" >&#43;</strong>
                    <strong class="vote--option" data-vote="down" data-project="${project.id}" >&#8722;</strong>
                </div>
                <i>${project.vote_ratio}% Positive Feedback</i>
                <p>${project.description.substring(0,150)}</p>

            </div>

        </div>
        `
        projectsWrapper.innerHTML += projectCard
    }
    addVoteEvent()
}

let addVoteEvent = () => {
    let voteBtn = document.getElementsByClassName('vote--option')
    for (let i = 0; i < voteBtn.length; i++) {
        voteBtn[i].addEventListener('click', function (e) {
            let vote = e.target.dataset.vote
            let project = e.target.dataset.project
            let token = localStorage.getItem('token')

            // fetch(`http://127.0.0.1:8000/api/project/${project}/vote/`,{
            //     method:'post',
            //     headers: {
            //         'Content-Type' : 'application/json',
            //         Authorization : `Bearer ${token}`,
            //         data : JSON.stringify({"value" : vote}),
            //         "Access-Control-Allow-Origin" : "*",
            //         "Access-Control-Allow-Methods" : "GET,POST,PUT,DELETE,OPTIONS",
            //         "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
            //     }
            // }).then(response => response.json())
            // .then((data) =>{
            //     getProject()
            // })

            try {
                var xhr = new XMLHttpRequest();
                xhr.open('POST', `http://127.0.0.1:8000/api/project/${project}/vote/`, true);
                xhr.setRequestHeader('Content-type', 'application/json');
                xhr.setRequestHeader("Authorization", `Bearer ${token}`);
                xhr.send(JSON.stringify({
                    "value": vote
                }));
                xhr.onreadystatechange = function (data) {
                    getProject()
                };
                xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
                xhr.setRequestHeader("Access-Control-Allow-Credentials", "true");
                xhr.setRequestHeader("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT");
                xhr.setRequestHeader("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers");
            } catch (error) {

            }

        })
    }
}


getProject()