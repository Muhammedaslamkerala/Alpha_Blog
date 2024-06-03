document.getElementById('comment-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var comment = document.getElementById('comment').value;

    if (comment) {
        var commentElement = document.createElement('div');
        commentElement.classList.add('comment');

        var authorElement = document.createElement('div');
        authorElement.classList.add('comment-author');
        authorElement.innerText = 'Anonymous'; // Default to Anonymous

        var textElement = document.createElement('div');
        textElement.classList.add('comment-text');
        textElement.innerText = comment;

        commentElement.appendChild(authorElement);
        commentElement.appendChild(textElement);

        document.getElementById('comments-list').appendChild(commentElement);

        document.getElementById('comment').value = '';
    }
});