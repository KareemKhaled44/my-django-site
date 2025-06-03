$(document).ready(function () {
  $(".filter-category").click(function (e) {
    e.preventDefault(); // تمنع التحويل للرابط

    let cid = $(this).data("cid");

    console.log("Clicked category URL:", cid);

  
    $.ajax({
      url: "/async/category-product-list/" + cid + "/",
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
      beforesend: function () {
        console.log("Loading...");
      },
      success: function (data) {
        // هنا تحط الكود اللي يعرض المنتجات بدون ما تعمل reload
        $("#product-container").html(data.html);
        console.log("Products loaded successfully");
        console.log("Products HTML:", data.html);
        $("#pagination-container").html(data.pagination);
        console.log("Pagination loaded successfully");
        console.log("Pagination HTML:", data.pagination);

      },
      error: function () {
        console.log("Something went wrong");
      },
     
    });
  });

  $(document).on("click", ".pagination-link", function (e) {
    e.preventDefault();

    const page_url = $(this).attr("href");

    $.ajax({
      url: page_url,
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
      success: function (data) {
        $("#product-container").html(data.html);
        $("#pagination-container").html(data.pagination);
      },
      error: function () {
        console.log("Pagination load failed");
      },
    });
  });
});





