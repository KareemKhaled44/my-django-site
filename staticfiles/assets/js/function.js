$(document).ready(function () {
  var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
  if (csrftoken) {
    $.ajaxSetup({
      headers: { "X-CSRFToken": csrftoken },
    });
  }
  // Function for pagination
  // Only apply ajax pagination if NOT in admin dashboard
  if (!window.location.pathname.includes('useradmin')) {
  $(document).on("click", ".pagination-link", function (e) {
    e.preventDefault();

    const page_url = $(this).attr("href");
    showSpinner();
    $.ajax({
      url: page_url,
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
      success: function (data) {
        //smooth scroll to top
        $("html, body").animate(
          {
            scrollTop: $("#product-container").offset().top - 60,
          },
          500
        );
        setTimeout(function () {
          hideSpinner();

          $("#product-container").html(data.html);
          $("#pagination-container").html(data.pagination);
        }, 500);
      },
      error: function () {
        console.log("Pagination load failed");
      },
    });
  });
  }

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
  $(".add-to-cart-btn").on("click", function () {
    let this_val = $(this);

    let product_card = this_val.closest(".card");
    let productId = product_card.find(".product-id").val();
    let quantity = product_card.find(".product-quantity").val();
    let product_title = product_card.find(".product-title").text();
    let product_price = product_card.find(".current-product-price").text();
    let product_image = product_card.find(".product-image").attr("src");
    let product_flavor = product_card.find(".product-flavor").val();

    showSpinner();
    $.ajax({
      url: "/add-to-cart/",
      data: {
        pid: productId,
        quantity: quantity,
        product_title: product_title,
        product_price: product_price,
        product_image: product_image,
        product_flavor: product_flavor,
      },
      success: function (response) {
        setTimeout(function () {
          hideSpinner();
          this_val.html("<span style='color:#28282B'>✔</span>");
          $("#cart-items-count").text(response.cart_total_items);

          // Chain the second AJAX call to update the mini cart
          $.ajax({
            url: "/update-cart-preview/",
            success: function (res) {
              console.log("Cart preview updated successfully");
              $("#cart-preview-container").html(res.cart_preview_html);
            },
          });
        }, 500);
      },
    });
  });

  // Function to delete from cart
  $(document).on("click", ".delete-product", function () {
    let productId = $(this).attr("data-pid");
    let this_val = $(this);

    console.log("Deleting product with ID:", productId);
    showSpinner();
    $.ajax({
      url: "/delete-from-cart/",
      data: {
        pid: productId,
      },
      beforeSend: function () {
        console.log("Deleting from cart...");
        this_val.hide();
      },
      success: function (response) {
        setTimeout(function () {
          hideSpinner();
          console.log("Product deleted from cart successfully");
          
          if (response.shipping_cost === 0) {
            $("#shipping_cost").html(
              "<span class='text-green-500 font-semibold'>Free</span>"
            );
          } else {
            $("#shipping_cost").text("EGP " + response.shipping_cost);
          }

          // Update the total amount in the cart summary
          $("#cart_total_amount").text("EGP " + response.cart_total_amount);

          $("#cart-items-count").text(response.cart_total_items);
          this_val.closest("tr[id^='cart-item']").fadeOut(300, function () {
            $(this).remove();
          });
        }, 500);
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

    showSpinner();
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
        setTimeout(function () {
          hideSpinner();
          $("#cart-items-count").text(response.cart_total_items);
          // Update the total price for the specific cart item
          $(`#subtotal-${productId}`).text(`EGP ${response.item_subtotal}`);

          // Update shipping cost if applicable
          if (response.shipping_cost === 0) {
            $("#shipping_cost").html("<span class='text-green-500 font-semibold'>Free</span>");
          } else {
            $("#shipping_cost").text("EGP " + response.shipping_cost);
          }

          // Update the total amount in the cart summary
          $("#cart_total_amount").text("EGP " + response.cart_total_amount);

          console.log("Cart item updated successfully");
        }, 400);
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
    showSpinner();
    $.ajax({
      url: "/apply-coupon/",
      data: {
        coupon_code: couponCode,
      },
      beforesend: function () {
        console.log("Applying coupon...");
      },
      success: function (response) {
        setTimeout(function () {
          hideSpinner();
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
        }, 500);
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
    let phone = $("#phone").val();
    showSpinner();
    $.ajax({
      url: "/Ajax_contact_form/",
      type: "POST",
      data: {
        full_name: full_name,
        email: email,
        subject: subject,
        message: message,
        phone: phone,
      },

      beforeSend: function () {
        console.log("Sending contact form...");
      },
      success: function (response) {
        setTimeout(function () {
          hideSpinner();
          if (response.success) {
            console.log("Contact form submitted successfully");
            showMessage(response.message, "success");
            $("#contact-form")[0].reset();
          } else {
            console.log("Failed to submit contact form");
            showMessage(response.message, "error");
          }
        }, 1000);
      },
      error: function () {
        console.log("Error submitting contact form");
      },
    });
  });

  // Function to make address as default
  $(document).on("click", ".make-default-btn", function (e) {
    e.preventDefault();
    let Id = $(this).attr("data-id");
    let this_val = $(this);
    console.log(" ID:", Id);
    console.log("this_val:", this_val);
    showSpinner();
    $.ajax({
      url: "/make-default-address/",
      data: {
        id: Id,
      },
      method: "GET",
      beforeSend: function () {
        console.log("Making address default...");
        this_val.hide();
      },
      success: function (response) {
        setTimeout(function () {
          if (response.success) {
            hideSpinner();
            // اخفي كل الايقونات والزرار
            $(".check-btn").hide();
            $(".make-default-btn").show();

            // بعدين أظهر الايقونة الخاصة بالعنصر اللي اختاره
            this_val.prev(".check-btn").show();
            this_val.hide();
          }
        }, 500);

        console.log("Address made default successfully");
      },
      error: function () {
        console.log("Error making address default");
      },
    });
  });

  // Function to delete address
  $(document).on("click", "#delete-address", function (e) {
    e.preventDefault();
    let Aid = $(this).attr("data-address-id");
    let this_val = $(this);
    console.log("Deleting address with ID:", Aid);
    $.ajax({
      url: "/delete-address/",
      data: {
        aid: Aid,
      },
      beforeSend: function () {
        console.log("Deleting address...");
        this_val.hide();
      },
      success: function (response) {
        if (response.success) {
          console.log("Address deleted successfully");

          // Remove the whole address card (container) from the DOM
          this_val.closest(".address-card").fadeOut(300, function () {
            $(this).remove();
          });

          showMessage(response.message, "success");
        }
      },
      error: function () {
        console.log("Error deleting address");
      },
    });
  });

  // function to add to wishlist
  $(document).on("click", ".add-to-wishlist", function (e) {
    e.preventDefault();
    let productId = $(this).attr("data-pid");
    let this_val = $(this);
    showSpinner();
    console.log("Adding to wishlist product with ID:", productId);
    $.ajax({
      url: "/add_to_wishlist/",
      data: {
        pid: productId,
      },
      beforeSend: function () {
        console.log("Adding to wishlist...");
      },
      success: function (response) {
        if (response.success) {
          setTimeout(function () {
            console.log("Product added to wishlist successfully");
            this_val.html("<i class='fa-solid fa-heart text-gold'></i>");

            showMessage(response.message, "success");
            hideSpinner();
          }, 400);
        } else {
          setTimeout(function () {
            console.log("Product already in wishlist");
            showMessage(response.message, "success");
            hideSpinner();
          }, 400);
        }
      },
      error: function () {
        console.log("Error adding product to wishlist");
      },
    });
  });

  // function to delete from wishlist
  $(document).on("click", ".delete-from-wishlist", function (e) {
    e.preventDefault();
    let productId = $(this).attr("data-pid");
    let this_val = $(this);
    console.log("Deleting from wishlist product with ID:", productId);
    showSpinner();
    $.ajax({
      url: "/delete_from_wishlist/",
      data: {
        pid: productId,
      },
      beforeSend: function () {
        console.log("Deleting from wishlist...");
        this_val.hide();
      },
      success: function (response) {
        if (response.success) {
          setTimeout(function () {
            console.log("Product deleted from wishlist successfully");

            this_val.closest(".wishlist-card").fadeOut(300, function () {
              $(this).remove();
            });
            showMessage(response.message, "success");
            hideSpinner();
          }, 400);
        } else {
          setTimeout(function () {
            console.log("Error deleting product from wishlist");
            showMessage(response.message, "error");
            hideSpinner();
          }, 400);
        }
      },
      error: function () {
        console.log("Error deleting product from wishlist");
      },
    });
  });
});