document.addEventListener("DOMContentLoaded", () => {
  const openSidebar = document.getElementById("openSidebar");
  const closeSidebar = document.getElementById("closeSidebar");
  const sidebar = document.getElementById("sidebar");

  // Function to open sidebar
  function openMenu() {
    sidebar.classList.remove("-translate-x-full");
    openSidebar.classList.add("hidden"); // Hide the ☰ button
  }

  // Function to close sidebar
  function closeMenu() {
    sidebar.classList.add("-translate-x-full");
    openSidebar.classList.remove("hidden"); // Show the ☰ button again
  }

  // Open Sidebar
  openSidebar.addEventListener("click", (e) => {
    e.stopPropagation(); // Prevent event from bubbling up
    openMenu();
  });

  // Close Sidebar (only if closeSidebar exists)
  if (closeSidebar) {
    closeSidebar.addEventListener("click", (e) => {
      e.stopPropagation();
      closeMenu();
    });
  }

  // Close Sidebar When Clicking Outside
  document.addEventListener("click", (event) => {
    if (
      !sidebar.contains(event.target) &&
      !openSidebar.contains(event.target)
    ) {
      closeMenu();
    }
  });

  // Prevent sidebar from closing when clicking inside
  sidebar.addEventListener("click", (e) => e.stopPropagation());
});
