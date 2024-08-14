document.addEventListener('DOMContentLoaded', function () {
    const allStar = document.querySelectorAll('.rating .star');
    const ratingValue = document.querySelector('.rating input');
    const currentRating = parseInt(ratingValue.value); // Get the current rating from the hidden input

    function updateStars(rating) {
        allStar.forEach((star, idx) => {
            if (idx < rating) {
                star.classList.add('selected');
            } else {
                star.classList.remove('selected');
            }
        });
    }

    function setRating(rating) {
        ratingValue.value = rating;
        updateStars(rating);
    }

    // Initialize stars based on current rating
    updateStars(currentRating);

    allStar.forEach((item, idx) => {
        item.addEventListener('click', function () {
            const newRating = idx + 1;
            setRating(newRating);
        });
    });
});
