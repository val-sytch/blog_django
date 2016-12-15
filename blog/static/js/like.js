(function(){

    var isLoading = false;

    var btns = document.querySelectorAll('button.likes');

    for(var i = 0; i < btns.length; i++){
        btns[i].addEventListener('click', likePost);
    }


    function likePost(event){
        var el = this,
            action = el.getAttribute('data-action'),
            post = el.getAttribute('data-post');

        if(action == 'like-post' && isLoading != true){

            isLoading = !isLoading;


            var xhr = new XMLHttpRequest(),
                params = '?action=' + encodeURIComponent(action) + '&post=' + encodeURIComponent(post);

            xhr.open('GET', '/likes' + params);
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

            xhr.send();

            xhr.onload = function() {
                if (xhr.status >= 200 && xhr.status < 400) {
                    var response = xhr.responseText,
                        count = el.querySelector('span.count');

                    response = JSON.parse(response);

                    response.is_liked ? el.classList.add('liked') : el.classList.remove('liked');
                    count.innerHTML = response.num_likes;
                    isLoading = !isLoading;
                }
                else {

                }
            };

        }

    }

})();

