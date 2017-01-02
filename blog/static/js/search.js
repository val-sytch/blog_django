(function(){

    var isLoading = false;

    var input = document.getElementById('search-form-input');


        input.addEventListener('keyup', searchTitleText);


    function searchTitleText(event){

        if(input.value.length != 0 && isLoading != true){

            isLoading = !isLoading;


            var xhr = new XMLHttpRequest(),
                params = '?query=' + encodeURIComponent(this.value);

            xhr.open('GET', '/search' + params);
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

            xhr.send();

            xhr.onload = function() {
                if (xhr.status >= 200 && xhr.status < 400) {
                    var content = document.getElementById('main-content-block');
                    content.innerHTML = xhr.responseText;

                    isLoading = !isLoading;
                }
                else {

                }
            };

        }

    }

})();

