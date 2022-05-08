let searchForm = document.getElementById('searchForm')
let pageLink = document.getElementsByClassName('pageLink')

if(searchForm){
    for(let i=0; i < pageLink.length;i++ ){
        pageLink[i].addEventListener('click',function(e){
            e.preventDefault()
            let page = this.dataset.page
            searchForm.innerHTML += `<input  name="page"
                    value="${page}" hidden />`
            searchForm.submit()
        })
    }
}