// ---------------------------------------------------------
// GLOBAL STATE
// ---------------------------------------------------------
let cachedResult = null;
let lastPlatform = null;
let lastBrand = null;
let currentMetric = "followers"; // NEW → followers | engagement | impression

// Form Elements
const form = document.getElementById("statsForm");
const submitBtn = document.getElementById("submitBtn");
const loadingSpinner = document.getElementById("loadingSpinner");
const buttonText = document.querySelector(".button-text");
const platformSelect = document.getElementById("platform");
const brandSelect = document.getElementById("brand");
const rangeSelect = document.getElementById("range");

// ---------------------------------------------------------
// SUBMIT HANDLER (PLATFORM + BRAND ONLY)
// ---------------------------------------------------------
form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const platform = platformSelect.value;
    const brand = brandSelect.value;
    const range = rangeSelect.value;

    if (!platform || !brand || !range) {
        alert("Please fill all fields before submitting.");
        return;
    }

    // If platform + brand unchanged → USE CACHE
    if (platform === lastPlatform && brand === lastBrand) {
        renderStats(cachedResult, range);
        return;
    }

    // Fetch new data
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

        cachedResult = await res.json();
        renderStats(cachedResult, range);

        lastPlatform = platform;
        lastBrand = brand;

    } catch (err) {
        console.error(err);
        alert("Error fetching data.");
    } finally {
        loadingSpinner.classList.add("hidden");
        buttonText.textContent = "Submit";
        submitBtn.disabled = false;
    }
});

// ---------------------------------------------------------
// RENDER STATS FOR ALL ROWS
// ---------------------------------------------------------
function renderStats(result, range) {
    const container = document.getElementById("multiCurrencyStats");
    container.innerHTML = "";

    const btnContainer = document.getElementById("rangeButtons");
    btnContainer.classList.toggle("hidden", result.meta.row.length === 0);

    const brandQueried = result.meta.brand_queried.toUpperCase();

    result.meta.row.forEach((row) => {
        const latest = row.data[0];

        let followersGain = latest.daily_followers_gain;
        let impressionsGain = latest.daily_impressions;
        let engagementGain = latest.daily_engagements;

        if (range.toLowerCase() === "monthly") {
            followersGain = latest.total_followers;
            impressionsGain = latest.monthly_impressions;
            engagementGain = latest.monthly_engagements;
        }

        if (range.toLowerCase() === "weekly") {
            const weekly = row.data.slice(0, 7);
            followersGain = weekly.reduce((s, x) => s + (x.daily_followers_gain || 0), 0);
            impressionsGain = weekly.reduce((s, x) => s + (x.daily_impressions || 0), 0);
            engagementGain = weekly.reduce((s, x) => s + (x.daily_engagements || 0), 0);
        }

        // Store all values for graph switching
        const chartData = row.data.map(d => ({
            date: d.date,
            total_followers: d.total_followers,
            daily_impressions: d.daily_impressions,
            daily_engagements: d.daily_engagements,
            monthly_impressions: d.monthly_impressions,
            monthly_engagements: d.monthly_engagements
        }));

        createStatsCard({
            brand: `${brandQueried} - ${row.value}`,
            range: range + " Overview",
            followersGain,
            impressionsGain,
            engagementGain,
            chartData
        });
    });
}

// ---------------------------------------------------------
// CREATE CARD WITH CHART + SLIDER
// ---------------------------------------------------------
function createStatsCard(data) {
    const template = document.getElementById("statsCardTemplate");
    const clone = template.content.cloneNode(true);

    clone.querySelector(".card-title").textContent = data.brand;
    clone.querySelector(".card-range").textContent = data.range;
    clone.querySelector(".card-followers-gain").textContent = data.followersGain.toLocaleString();
    clone.querySelector(".card-engagement-gain").textContent = data.engagementGain.toLocaleString();
    clone.querySelector(".card-impressions-gain").textContent = data.impressionsGain.toLocaleString();

    const container = document.getElementById("multiCurrencyStats");
    container.appendChild(clone);

    const card = container.lastElementChild;
    const canvas = card.querySelector(".statsChart");
    const ctx = canvas.getContext("2d");

    const titleEl = card.querySelector(".chart-title");

    switch (currentMetric) {
        case "followers":
            titleEl.textContent = "Total Followers";
            break;
        case "engagement":
            titleEl.textContent = "Total Engagement";
            break;
        case "impression":
            titleEl.textContent = "Total Impressions";
            break;
    }

    const fullLabels = data.chartData.map(i => i.date).reverse();

    // CHOOSE GRAPH METRIC
    let fullValues = [];

    switch (currentMetric) {
        case "followers":
            fullValues = data.chartData.map(i => i.total_followers).reverse();
            break;
        case "engagement":
            fullValues = data.chartData.map(i => i.monthly_engagements || 0
            ).reverse();
            break;
        case "impression":
            fullValues = data.chartData.map(i => i.monthly_impressions || 0
            ).reverse();
            break;
    }
    

    // CREATE CHART
    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: fullLabels,
            datasets: [
                {
                    label: currentMetric.toUpperCase(),
                    data: fullValues,
                    borderColor: "#32cd32",
                    backgroundColor: "rgba(50,205,50,0.2)",
                    fill: true,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } }
        }
    });

    setTimeout(() => chart.resize(), 150);

    // SLIDER SETUP
    const sliderDiv = card.querySelector(".date-slider");
    const sliderLabel = card.querySelector(".slider-range-label");

    const total = fullLabels.length;
    const lastIndex = total - 1;
    const startIndex = Math.max(0, lastIndex - 6);

    noUiSlider.create(sliderDiv, {
        start: [startIndex, lastIndex],
        connect: true,
        step: 1,
        range: { min: 0, max: lastIndex }
    });

    sliderLabel.textContent = `${fullLabels[startIndex]} → ${fullLabels[lastIndex]}`;

    chart.data.labels = fullLabels.slice(startIndex, lastIndex + 1);
    chart.data.datasets[0].data = fullValues.slice(startIndex, lastIndex + 1);
    chart.update();

    sliderDiv.noUiSlider.on("update", (values) => {
        const s = Math.round(values[0]);
        const e = Math.round(values[1]);

        chart.data.labels = fullLabels.slice(s, e + 1);
        chart.data.datasets[0].data = fullValues.slice(s, e + 1);
        chart.update();

        sliderLabel.textContent = `${fullLabels[s]} → ${fullLabels[e]}`;
    });
}

// ---------------------------------------------------------
// RANGE CHANGED (NO FETCH)
// ---------------------------------------------------------
rangeSelect.addEventListener("change", () => {
    if (cachedResult) renderStats(cachedResult, rangeSelect.value);
});

// ---------------------------------------------------------
// METRIC SWITCH BUTTONS
// ---------------------------------------------------------
document.getElementById("btnFollowers").onclick = () => switchMetric("followers");
document.getElementById("btnEngagement").onclick = () => switchMetric("engagement");
document.getElementById("btnImpression").onclick = () => switchMetric("impression");

function switchMetric(metric) {
    currentMetric = metric;
    if (cachedResult) renderStats(cachedResult, rangeSelect.value);
}
