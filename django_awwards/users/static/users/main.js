window.onload = () => {
    const route = window.location.pathname
    const header = document.querySelector('header')
    if (route === '/') {
        header.style.backgroundColor = 'rgba(0, 0, 0, 0.479)'
    }

    // ratings functionality
    const ratingBtns = document.querySelectorAll('.ratings span')
    ratingBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const postID = parseInt(document.querySelector('.ratings').dataset.postid)
            const ratingValue = parseInt(e.target.dataset.value)
            fetch(`/rate/${postID}/?value=${ratingValue}`)
                .then(res => res.json())
                .then(data => {
                    if (data.status_code === 302) {
                        window.location.pathname = '/login'
                    }

                    else {
                        document.querySelector('.ratings').innerHTML = '<p>You have already rated this site!</p>'
                        console.log(document.querySelector('.ratings'))
                        alert('site rated!')
                    }
                })
        })
    })

    // search sites functionality
    const searchInput = document.querySelector('#search-wrapper input')
    const searchBtn = document.querySelector('#search-wrapper i')
    searchBtn.onclick = (e) => {
        const query = searchInput.value
        window.location.href = window.location.origin + `/posts/filtered/${query}/`
    }
}