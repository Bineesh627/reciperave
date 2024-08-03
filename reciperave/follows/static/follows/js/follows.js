// static/js/scripts.js

function followUser(uid) {
    fetch(`/follow_user/?id=${uid}`)
        .then(response => {
            if (response.ok) {
                window.location.reload();  // Reload the page to update follow status
            } else {
                alert('Error following user.');
            }
        })
        .catch(error => console.error('Error:', error));
}

function unfollowUser(uid) {
    fetch(`/unfollow_user/?id=${uid}`)
        .then(response => {
            if (response.ok) {
                window.location.reload();  // Reload the page to update follow status
            } else {
                alert('Error unfollowing user.');
            }
        })
        .catch(error => console.error('Error:', error));
}
