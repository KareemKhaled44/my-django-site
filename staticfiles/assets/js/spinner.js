// spinner
function showSpinner() {
  console.log("showing spinner");
  let spinnerHtml = `
      <div class="animate-spin rounded-full h-10 w-10 border-t-4 border-b-4 border-[#b9a848]"></div>
      `;
  let spinnerContainer = $("#spinner-container");
  spinnerContainer.html(spinnerHtml);
  spinnerContainer.css({
    display: "flex",
    "justify-content": "center",
    "align-items": "center",
    position: "fixed",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    "z-index": "9999",
    "background-color": "rgba(0, 0, 0, 0.5)",
    width: "100%",
    height: "100%",
  });
}

function hideSpinner() {
  console.log("hiding spinner");
  let spinnerContainer = $("#spinner-container");
  spinnerContainer.css({
    display: "none",
  });
}
