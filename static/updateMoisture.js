function updateMoisture() {
  fetch("/moisture")
    .then((response) => response.json())
    .then((data) => {
      data.forEach((item) => {
        if (item.ID === 1) {
          document.getElementById(
            "plant1"
          ).textContent = `moisture: ${item.Moisture}`;
        } else if (item.ID === 2) {
          document.getElementById(
            "plant2"
          ).textContent = `moisture:${item.Moisture}`;
        }
      });
    })
    .catch((error) => {
      console.error("Error fetching moisture data:", error);
    });
}

setInterval(updateMoisture, 1000);
