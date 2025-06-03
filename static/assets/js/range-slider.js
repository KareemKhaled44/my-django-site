const sliderElement = document.getElementById('price-slider');
const minPrice = parseInt(sliderElement.dataset.min);
const maxPrice = parseInt(sliderElement.dataset.max);

noUiSlider.create(sliderElement, {
  start: [minPrice, maxPrice],
  connect: true,
  range: {
    min: minPrice,
    max: maxPrice
  },
  step: 10,
  format: {
      to: function (value) {
        return Math.round(value);
      },
      from: function (value) {
        return Number(value);
      }
    }

    
  });

  const minDisplay = document.getElementById("min-value");
  const maxDisplay = document.getElementById("max-value");

  sliderElement.noUiSlider.on("update", function (values, handle) {
    minDisplay.innerHTML = "min: " + values[0] + " EGP";
    maxDisplay.innerHTML = "max: " + values[1] + " EGP";
  });