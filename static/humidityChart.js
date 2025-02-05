// Create the chart
const aqchart = Highcharts.chart("chart1", {
  chart: {
    type: "line",
    animation: Highcharts.svg,
    marginRight: 10,
    events: {
      load: function () {
        // Set up the updating of the chart each second
        const series = this.series[0]; // Only one series for humidity
        setInterval(() => {
          fetch("/data")
            .then((response) => response.text())
            .then((csv) => {
              const rows = csv.trim().split("\n");
              const data = rows
                .slice(1) // Skip the header row
                .map((row) => row.split(",").map(parseFloat)); // Convert each value to a float

              // Simulate live data update
              const latest = data[data.length - 1]; // Get the latest row
              const currentTime = new Date();
              const gmt3Time = new Date(
                currentTime.getTime() + 3 * 60 * 60 * 1000
              ); // Adjust to GMT+3
              const x = gmt3Time.getTime();
              const humidity = latest[1]; // Second column is Humidity

              // Add the point to the series
              series.addPoint([x, humidity], true, true);
            })
            .catch((error) => console.error("Error loading CSV data:", error));
        }, 1000); // Update every second
      },
    },
  },
  title: {
    text: "Humidity levels",
  },
  subtitle: {
    text: "numbers are taken from the DHT-11 sensor",
  },
  xAxis: {
    type: "datetime",
    tickPixelInterval: 300,
    /* datetime axes are based on milliseconds, so for example an interval of one day is expressed as 24 * 3600 * 1000.  */
    gridLineWidth: 1,
  },
  yAxis: {
    title: {
      text: "Humidity Level",
    },
    gridLineWidth: 1,
  },
  tooltip: {
    formatter: function () {
      return `
      ${Highcharts.numberFormat(this.y, 2)}
      <br/>${Highcharts.dateFormat("%[YebHM]", this.x)}
      `;
    },
  },
  legend: {
    enabled: true,
  },
  exporting: {
    enabled: true,
  },
  series: [
    /*   {
      name: "Temperature",
      data: (function () {
        // Generate initial data
        const data = [];
        const time = new Date().getTime();
        for (let i = -19; i <= 0; i += 1) {
          data.push({
            x: time + i * 1000,
            y: 23.0, // Default initial value
          });
        }
        return data;
      })(),
    }, */
    {
      name: "Humidity",
      color: "#0D5956",
      data: (function () {
        // Generate initial data
        const data = [];
        const time = new Date().getTime();
        for (let i = -19; i <= 0; i += 1) {
          data.push({
            x: time + i * 1000,
            y: 0.0, // Default initial value
          });
        }
        return data;
      })(),
    },
  ],
});
