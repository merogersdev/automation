// Event Listeners

const diskUsage = document.querySelector("#disk-usage");
const cpuUsage = document.querySelector("#cpu-usage");
const reboot = document.querySelector("#reboot");
const cpuTemp = document.querySelector("#cpu-temp");
const internet = document.querySelector("#internet");
const cpuLoad = document.querySelector("#cpu-load");
const memoryUsage = document.querySelector("#memory-usage");

function renderBooleanResult(element, result, success_message, fail_message) {
  if (result) {
    element.innerText = success_message;
    element.setAttribute("class", "text-danger");
  } else {
    element.innerText = fail_message;
    element.setAttribute("class", "text-success");
  }
}

function renderStats(data) {
  renderBooleanResult(reboot, data.system.reboot, "Yes", "No");
  renderBooleanResult(internet, data.system.internet, "Failure", "Success");
  renderBooleanResult(
    memoryUsage,
    data.memory.over,
    `Current: ${data.memory.usage}%`,
    `Current: ${data.memory.usage}%`
  );

  renderBooleanResult(
    diskUsage,
    data.disk.disk_over,
    `${data.disk.gb_free}GB/${data.disk.gb_total}GB, ${data.disk.percent_free}% Free`,
    `${data.disk.gb_free}GB/${data.disk.gb_total}GB, ${data.disk.percent_free}% Free`
  );
  renderBooleanResult(
    cpuUsage,
    data.cpu.over,
    `Current: ${data.cpu.usage}%`,
    `Current: ${data.cpu.usage}%`
  );
  renderBooleanResult(
    cpuLoad,
    data.cpu.load_avg_over,
    `1 Min: ${data.cpu.load_avg.one_min}% / 5 Min ${data.cpu.load_avg.five_min}% / 15 Min ${data.cpu.load_avg.fifteen_min}%`,
    `1 Min: ${data.cpu.load_avg.one_min}% / 5 Min ${data.cpu.load_avg.five_min}% / 15 Min ${data.cpu.load_avg.fifteen_min}%`
  );
}

// Display the results to the dashboard
async function fetchStats() {
  fetch("/api/v1/")
    .then((res) => res.json())
    .then((data) => renderStats(data));
}

function init() {
  fetchStats();

  setInterval(async function () {
    fetchStats();
  }, 10000);
}

// Run Render after DOM is loaded
document.addEventListener("DOMContentLoaded", init);
