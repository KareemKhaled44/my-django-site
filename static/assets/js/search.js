const openSearch = document.getElementById("openSearch");
const closeSearch = document.getElementById("closeSearch");
const searchOverlay = document.getElementById("searchOverlay");
const searchInput = document.getElementById("searchInput");

// Open search
openSearch.addEventListener("click", () => {
  searchOverlay.classList.remove("hidden");
  document.getElementById("mobileMenu").classList.remove("active");
  searchInput.focus();
});

// Close search
closeSearch.addEventListener("click", () => {
  searchOverlay.classList.add("hidden");
});

// Close on ESC key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    searchOverlay.classList.add("hidden");
  }
});
