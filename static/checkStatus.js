// Function to update the status dynamically
function updateStatus() {
  fetch("/status")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("status").innerText = `Status: ${data.status}`;
    })
    .catch((error) => {
      console.error("Error fetching status:", error);
      document.getElementById("status").innerText = "Status: Error";
    });
}

// Update status every second
setInterval(updateStatus, 1000);
