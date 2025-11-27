document.addEventListener("DOMContentLoaded", function () {
    var platformSelect = document.getElementById("platform");
    var brandSelect = document.getElementById("brand");

    // Define brands for each platform
    var platformBrands = {
        Facebook: ["BAJI", "SIX6S", "JEETBUZZ", "BADSHA"],
        Instagram: ["BAJI", "SIX6S", "JEETBUZZ", "BADSHA"],
        Twitter: ["BAJI", "SIX6S", "JEETBUZZ", "BADSHA", "BJ SPORTS", "HD MOVIE"],
        Youtube: ["BAJI", "SIX6S", "JEETBUZZ", "BADSHA"]
    };

    function updateBrands() {
        var selectedPlatform = platformSelect.value;
        var brands = platformBrands[selectedPlatform] || [];

        // Clear current options
        brandSelect.innerHTML = "";

        // Add a placeholder option
        var placeholder = document.createElement("option");
        placeholder.textContent = "Select Brand";
        placeholder.value = "";
        brandSelect.appendChild(placeholder);

        // Populate new options
        for (var i = 0; i < brands.length; i++) {
            var option = document.createElement("option");
            option.value = brands[i];
            option.textContent = brands[i];
            brandSelect.appendChild(option);
        }
    }

    // Update brands on page load
    updateBrands();

    // Update brands whenever platform changes
    platformSelect.addEventListener("change", updateBrands);
});
