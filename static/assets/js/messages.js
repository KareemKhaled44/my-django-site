function showMessage(message, type = "info") {
  console.log("Function entered");

  let colorClass = "";

  if (type === "success") {
    colorClass = "border-green-500";
  } else if (type === "error") {
    colorClass = "border-red-500";
  } else if (type === "warning") {
    colorClass = "border-[#b9a848]";
  } else {
    colorClass = "border-blue-500";
  }

  let messageHtml = `
    <div class="alert px-5 py-3 rounded-xl shadow-lg min-w-[300px] max-w-md text-center transition-opacity duration-300 bg-[#28282B] border-l-4 ${colorClass}">
        <p class="text-[#ebebeb] text-sm font-medium">${message}</p>
    </div>
  `;

  $("#messages-container").append(messageHtml);

  setTimeout(() => {
    let alert = $("#messages-container .alert").last();
    alert.css("transition", "opacity 0.5s ease");
    alert.css("opacity", "0");
    setTimeout(() => alert.remove(), 500);
  }, 3000);
}
// spinner


