document.addEventListener("DOMContentLoaded", function() {
    const searchBar = document.querySelector(".search-bar");
  
    searchBar.addEventListener("focus", function() {
        this.style.border = "2px solid #ff4b5c";
    });
  
    searchBar.addEventListener("blur", function() {
        this.style.border = "none";
    });
  
    document.querySelectorAll(".menu-item").forEach(button => {
        button.addEventListener("click", () => {
            alert(`Navigating to ${button.textContent}...`);
        });
    });
  });
  