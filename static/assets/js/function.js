$(document).ready(function () {
  var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
  if (csrftoken) {
    $.ajaxSetup({
      headers: { "X-CSRFToken": csrftoken },
    });
  }
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
    let product_image = product_card.find(".product-image").attr('src');


    console.log("quantity:",quantity,
      "productId:", productId,
       "product_title:", product_title,
       "product_price:",  product_price,
       "product_image:", product_image
      );


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

  // Function to delete from cart
  $(document).on("click", ".delete-product", function () {
    let productId = $(this).attr("data-pid");
    let this_val = $(this);

    console.log("Deleting product with ID:", productId);

    $.ajax({
      url: "/delete-from-cart/",
      data: {
        pid: productId,
      },
      beforesend: function () {
        console.log("Deleting from cart...");
        this_val.hide();
      },
      success: function (response) {
        this_val.show();
        $("#cart-items-count").text(response.cart_total_items);
        $("#cart-list").html(response.data);
      },
      error: function () {
        console.log("Error deleting product from cart");
      },
    });
  });

  // Function to update cart item quantity
  $(document).on("click", ".update-cart", function () {
    let productId = $(this).attr("data-pid");
    let quantity = $(`#qty-${productId}`).val();
    let this_val = $(this);

    console.log("Updating product with ID:", productId, "to quantity:", quantity);

    $.ajax({
      url: "/update-cart-item/",
      data: {
        pid: productId,
        quantity: quantity,
      },
      beforesend: function () {
        console.log("Updating cart item...");
      },
      success: function (response) {
        $("#cart-items-count").text(response.cart_total_items);
        $("#cart-list").html(response.data);
      },
      error: function () {
        console.log("Error updating cart item");
      },
    });
  });  

  // Function to handle apply coupon button
  $("#apply-coupon-btn").on("click", function (e) {
    e.preventDefault();
    let couponCode = $("#coupon-code").val();

    console.log("Applying coupon code:", couponCode);

    $.ajax({
      url: "/apply-coupon/",
      data: {
        coupon_code: couponCode,
      },
      beforesend: function () {
        console.log("Applying coupon...");
      },
      success: function (response) {
        if (response.success) {
          console.log("Coupon applied successfully");
          $("#discount-amount").text("EGP - " + response.discount);
          $("#total-amount").text("EGP " + response.total_after_discount);

          $("#Subtotal-amount").html(
            '<span style="text-decoration: line-through;">EGP ' +
              response.cart_total_amount +
              "</span>"
          );

          $(".discount-section").show();
          $(".total-section").show();

          showMessage(response.message, "success");
        } else {
          console.log("Failed to apply coupon");
          showMessage(response.message, "error");
        }

        
      },
      error: function () {
        console.log("Error applying coupon");
      },
    });
  });

  // Function for contact form submission
  $("#contact-form").on("submit", function (e) {
    e.preventDefault();
    console.log("Contact form submitted");
    let full_name = $("#full_name").val();
    let email = $("#email").val();
    let subject = $("#subject").val();
    let message = $("#message").val();

    showSpinner();
    $.ajax({
      url: "/Ajax_contact_form/",
      type: "POST",
      data: {
        full_name: full_name,
        email: email,
        subject: subject,
        message: message,
      },

      beforeSend: function () {
        console.log("Sending contact form...");
        
      },
      success: function (response) {
        if (response.success) {
          console.log("Contact form submitted successfully");
          showMessage(response.message, "success");
          // Optionally clear the form
          $("#contact-form")[0].reset();
        } else {
          console.log("Failed to submit contact form");
          showMessage(response.message, "error");
        }
      },
      error: function () {
        console.log("Error submitting contact form");
      },
    });
  });
  
  
});





