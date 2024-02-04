// Function to hide the flash message
function hideFlashMessage() {
  const flashMessage = document.querySelector(".alert");
  if (flashMessage) {
    flashMessage.style.transition = "opacity 0.5s linear"; // this creates a fade-out effect
    flashMessage.style.opacity = "0"; // start the fade-out effect

    // Wait for the fade-out effect to finish before removing the element
    setTimeout(() => {
      flashMessage.remove();
    }, 500); // time in milliseconds (500ms for the fade-out effect)
  }
}

// Dismiss the flash message after 2 seconds
window.addEventListener("load", () => {
  setTimeout(hideFlashMessage, 2000); // 2000 milliseconds = 2 seconds
});

// reports
document.addEventListener("DOMContentLoaded", function () {
  var ctx = document.getElementById("progressReportChart").getContext("2d");
  var progressReportChart = new Chart(ctx, {
    type: "bar", // Change chart type as needed (bar, line, pie, etc.)
    data: {
      labels: ["Student 1", "Student 2", "Student 3"], // Example labels
      datasets: [
        {
          label: "Progress (%)",
          data: [75, 50, 90], // Example data
          backgroundColor: [
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
          ],
          borderColor: [
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
});
