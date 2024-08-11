const container = document.querySelector(".container");
const linkItems = document.querySelectorAll(".link-item");
const darkMode = document.querySelector(".dark-mode");
const logo = document.querySelector(".logo svg");

// Container Hover
container.addEventListener("mouseenter", () => {
  container.classList.add("active");
});

// Container Hover Leave
container.addEventListener("mouseleave", () => {
  container.classList.remove("active");
});

// Link-items Clicked
linkItems.forEach((item) => {
  if (!item.classList.contains("dark-mode")) {
    item.addEventListener("click", () => {
      linkItems.forEach((linkItem) => {
        linkItem.classList.remove("active");
      });
      item.classList.add("active");
    });
  }
});

// Dark Mode Functionality
const updateDarkModeButton = () => {
  if (document.body.classList.contains("dark-mode")) {
    darkMode.querySelector("span").textContent = "light mode";
    darkMode.querySelector("ion-icon").setAttribute("name", "sunny-outline");
    logo.style.fill = "#fff";
  } else {
    darkMode.querySelector("span").textContent = "dark mode";
    darkMode.querySelector("ion-icon").setAttribute("name", "moon-outline");
    logo.style.fill = "#363b46";
  }
};

// Toggle Dark Mode
darkMode.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  let isDarkMode = document.body.classList.contains('dark-mode');
  localStorage.setItem('darkMode', isDarkMode);
  updateDarkModeButton();
});

// Check preference on page load
document.addEventListener('DOMContentLoaded', () => {
  let isDarkMode = localStorage.getItem('darkMode') === 'true';
  if (isDarkMode) {
    document.body.classList.add('dark-mode');
  }
  updateDarkModeButton();
});
