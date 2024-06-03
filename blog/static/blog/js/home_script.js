function filterPosts(category) {
    var posts = document.querySelectorAll('.post');
    posts.forEach(function(post) {
        if (category === 'All' || post.getAttribute('data-category') === category) {
            post.style.display = 'block';
        } else {
            post.style.display = 'none';
        }
    });
}

function filterPostsByTag(tag) {
    var posts = document.querySelectorAll('.post');
    posts.forEach(function(post) {
        var tags = post.getAttribute('data-tags').split(',');
        if (tag === 'All' || tags.includes(tag)) {
            post.style.display = 'block';
        } else {
            post.style.display = 'none';
        }
    });
}

// Show all posts by default
filterPosts('All');