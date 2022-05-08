let form = document.getElementById('form-wrapper')
form.addEventListener('submit', (e)=> {
    e.preventDefault()
    formData = {
        'username' : document.getElementById('username').value,
        'password' : document.getElementById('password').value,
    }
    let url = 'http://127.0.0.1:8000/api/users/token/'
    fetch('http://127.0.0.1:8000/api/user/token/',{
        method : 'post',
        headers : {
            'Content-Type' : 'application/json',
        },
        body : JSON.stringify(formData)
    }).then(res => res.json())
    .then(data =>{
        if(data.access){
            localStorage.setItem('token',data.access)
            window.location = 'http://127.0.0.1:5500/index.html'
        }else{
            alert('username or password did not match')
        }
    })
}) 