const openSearch = document.getElementById("openSearch");
const closeSearch = document.getElementById("closeSearch");
const searchOverlay = document.getElementById("searchOverlay");
const searchInput = document.getElementById("searchInput");

// Open search
openSearch.addEventListener("click", () => {
  searchOverlay.classList.add("active");
  document.getElementById("mobileMenu").classList.remove("active");
  searchInput.focus();
});

// Close search
closeSearch.addEventListener("click", () => {
  searchOverlay.classList.remove("active");
});

// Close on ESC key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    searchOverlay.classList.remove("active");
  }
});



// Search Overlay Toggle 
    const input = document.getElementById("searchInput");
    const resultsBox = document.createElement("div");
    resultsBox.className = "absolute bg-white w-full z-50 rounded shadow-md";
    input.parentNode.appendChild(resultsBox);

    input.addEventListener("input", async () => {
      const q = input.value;
      if (!q) {
        resultsBox.innerHTML = "";
        return;
      }

      const res = await fetch(`/api/search-products/?q=${encodeURIComponent(q)}`);
      const data = await res.json();

      resultsBox.innerHTML = data.map(p => `
        <div class="flex items-center gap-3 p-2 hover:bg-gray-100 cursor-pointer z-90"
          onclick="window.location.href='/product/${p.id}/'">
          <img src="${p.image}" alt="${p.name}" class="w-12 h-12 object-cover rounded" />
          <div>
            <div class="font-semibold">${p.name}</div>
            <div class="text-sm text-gray-500">${p.price} EGP</div>
          </div>
        </div>
      `).join("");
    });
    