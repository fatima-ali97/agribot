function updateTemperature() {
  fetch("/ntemperature")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("ntemp").textContent = `${data.temperature}°C`;
      document.getElementById("time").textContent = `${data.time}`;
    })
    .catch((error) => {
      console.error("Error fetching temperature:", error);
      document.getElementById("temperature").textContent =
        "Error fetching data.";
    });
}

// Update status and temperature every second
setInterval(updateTemperature, 1000);
