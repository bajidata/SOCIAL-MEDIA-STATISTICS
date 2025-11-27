let cachedResult = null; // store fetched data here

const form = document.getElementById("statsForm");
const submitBtn = document.getElementById("submitBtn");
const loadingSpinner = document.getElementById("loadingSpinner");
const buttonText = document.querySelector(".button-text");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const platform = document.getElementById("platform").value;
    const brand = document.getElementById("brand").value;
    const range = document.getElementById("range").value;

    // Prevent submit if fields are empty
    if (!platform || !brand || !range) {
        alert("Please fill all fields before submitting.");
        return;
    }

    // Show loading spinner & disable button
    loadingSpinner.classList.remove("hidden");
    buttonText.textContent = "Loading...";
    submitBtn.disabled = true;

    const payload = { platform, brand, range };

    try {
        const res = await fetch("/api/stats", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        cachedResult = await res.json(); // save data
        renderStats(cachedResult, range);

    } catch (err) {
        console.error(err);
        alert("Error fetching data.");
    } finally {
        loadingSpinner.classList.add("hidden");
        buttonText.textContent = "Submit";
        submitBtn.disabled = false;
    }
});

// ------------------------------------------------------------------
// 🚀 RENDER FUNCTION (handles daily/weekly/monthly switching)
// ------------------------------------------------------------------
function renderStats(result, range) {
    const container = document.getElementById("multiCurrencyStats");
    container.innerHTML = "";

    const btnContainer = document.getElementById("rangeButtons");
    if (result.meta.row.length > 0) {
        btnContainer.classList.remove("hidden");
    } else {
        btnContainer.classList.add("hidden");
    }

    const template = document.getElementById("statsCardTemplate");
    const brandQueried = result.meta.brand_queried.toUpperCase();

    result.meta.row.forEach((row) => {
        const latest = row.data[0];

        // Default = daily values
        let followersGain = latest.daily_followers_gain;
        let impressionsGain = latest.daily_impressions;
        let engagementsGain = latest.daily_engagements;

        // ------- MONTHLY -------
        if (range.toLowerCase() === "monthly") {
            followersGain = latest.total_followers;
            impressionsGain = latest.monthly_impressions;
            engagementsGain = latest.monthly_engagements;
        }

        // ------- WEEKLY -------
        if (range.toLowerCase() === "weekly") {
            const weeklyData = row.data.slice(0, 7);
            followersGain = weeklyData.reduce((sum, d) => sum + (d.daily_followers_gain || 0), 0);
            impressionsGain = weeklyData.reduce((sum, d) => sum + (d.daily_impressions || 0), 0);
            engagementsGain = weeklyData.reduce((sum, d) => sum + (d.daily_engagements || 0), 0);
        }

        const clone = template.content.cloneNode(true);
        clone.querySelector(".card-title").textContent = `${brandQueried} - ${row.value}`;
        clone.querySelector(".card-range").textContent = range + " Overview";

        clone.querySelector(".card-followers-gain").textContent = followersGain.toLocaleString();
        clone.querySelector(".card-impressions-gain").textContent = impressionsGain.toLocaleString();
        clone.querySelector(".card-engagement-gain").textContent = engagementsGain.toLocaleString();

        container.appendChild(clone);
    });
}

// ------------------------------------------------------------------
// 🚀 AUTO SWITCH RANGE BUTTONS (NO BACKEND CALLS)
// ------------------------------------------------------------------
function autoSwitchRange(value) {
    document.getElementById("range").value = value;

    if (cachedResult) {
        renderStats(cachedResult, value); // reuse fetched data
    }
}

document.getElementById("btnDaily")?.addEventListener("click", () => autoSwitchRange("Daily"));
document.getElementById("btnWeekly")?.addEventListener("click", () => autoSwitchRange("Weekly"));
document.getElementById("btnMonthly")?.addEventListener("click", () => autoSwitchRange("Monthly"));
