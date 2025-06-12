$(document).ready(function () {
  // Function to apply filters and update product list
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

  $("#filter-button").click(function (e) {
    e.preventDefault();
    applyFilters(); 
  });

  $("#in-stock").change(function (e) {
    e.preventDefault();
    applyFilters();
  });

  $("#on-sale").change(function (e) {
    e.preventDefault();
    applyFilters();
  });

  $("#sort-by").change(function (e) {
    e.preventDefault();
    applyFilters();
  });
  
  $(".brand-filter").change(function (e) {
    e.preventDefault();
    applyFilters();
  });

  // add to cart functionality

  $(".add-to-cart-btn").on("click", function() {
    let this_val = $(this);

    // Use .closest to scope within the card
    let product_card = this_val.closest(".card");

    let productId = product_card.find(".product-id").val();
    let quantity = product_card.find(".product-quantity").val();
    let product_title = product_card.find(".product-title").text();
    let product_price = product_card.find(".current-product-price").text();
    let product_image = product_card.find(".product-image").val();

    console.log("quantity:",quantity,
      "productId:", productId,
       "product_title:", product_title,
       "product_price:",  product_price,
       "product_image:", product_image);


    $.ajax({
      url: "/add-to-cart/",
      data: {
        pid: productId,
        quantity: quantity,
        product_title: product_title,
        product_price: product_price,
        product_image: product_image
      },
      beforesend: function() {
        console.log("Adding to cart...");
      },
      success: function(response){
        console.log("Product added to cart successfully");
        this_val.html("<span style='color:#28282B'>✔</span>");

        $("#cart-items-count").text(response.cart_total_items);
      }
    });
  });

});





