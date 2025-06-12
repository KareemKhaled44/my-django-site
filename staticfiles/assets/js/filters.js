function getFilterData() {
  const values = sliderElement.noUiSlider.get();
  const min_price = values[0];
  const max_price = values[1];
  const cid = $("#filter-button").data("cid");
  const in_stock = $("#in-stock").is(":checked");
  const on_sale = $("#on-sale").is(":checked");
  const sort_by = $("#sort-by").val();
  const brands = [];$(".brand-filter:checked").each(function () { brands.push($(this).val());
 });

  let data = {
    min_price: min_price,
    max_price: max_price,
    in_stock: in_stock,
    on_sale: on_sale,
    sort_by: sort_by,
    brands: brands,
  };

  if (cid) {
    data.cid = cid;
  }

  return data;
}

function applyFilters() {
  const data = getFilterData();

  // URL جديد مع نفس path وباراميترات الكويري الأصلية (غير اللي هتعدلها)
  const url = new URL(window.location.href);

  // احتفظ بالـ path مع إضافة أو تعديل الباراميترات اللي ليها علاقة بالفلاتر
  url.searchParams.set("min_price", data.min_price);
  url.searchParams.set("max_price", data.max_price);
  url.searchParams.set("in_stock", data.in_stock);
  url.searchParams.set("on_sale", data.on_sale);
  url.searchParams.set("sort_by", data.sort_by);

  // حذف العلامة القديمة للبراندز قبل الإضافة
  url.searchParams.delete("brands[]");
  if (data.brands && data.brands.length > 0) {
    data.brands.forEach((brand) => {
      url.searchParams.append("brands[]", brand);
    });
  }

  $.ajax({
    url: url.toString(),
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
    beforeSend: function () {
      console.log("Filtering products...");
    },
    success: function (data) {
      $("#product-container").html(data.html);
      $("#pagination-container").html(data.pagination);
      console.log("Filtered products loaded successfully");
    },
    error: function () {
      console.log("Error while filtering products");
    },
  });
}
