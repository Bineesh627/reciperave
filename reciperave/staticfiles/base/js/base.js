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