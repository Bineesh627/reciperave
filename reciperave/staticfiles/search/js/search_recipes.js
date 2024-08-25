document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const filterSelect = document.getElementById('filterSelect');
    const cardContainer = document.querySelector('.card-container');
    
    function filterItems() {
        const searchValue = searchInput.value.toLowerCase();
        const filterValue = filterSelect.value;

        const cards = cardContainer.querySelectorAll('.recipe-card');

        cards.forEach(card => {
            const recipeName = card.querySelector('.card-recipe-content h3').textContent.toLowerCase();
            const dishType = card.querySelector('.card-recipe-content p').textContent.toLowerCase();

            const isTextMatch = recipeName.includes(searchValue);
            const isCategoryMatch = filterValue === "" || dishType.includes(filterValue.toLowerCase());

            if (isTextMatch && isCategoryMatch) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterItems);
    filterSelect.addEventListener('change', filterItems);
});
