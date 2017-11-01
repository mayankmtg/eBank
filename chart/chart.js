// var json_string = "{{json_list | safe | escapejs}}";
// var json_data = JSON.parse(json_string);

// Our labels along the x-axis
var dates = [1500,1600,1700,2050,1750,1800,1850,1900,1950,1999];
// For drawing the lines
// y-axis
var from_transactions = [86,114,106,2478,106,107,111,133,221,783];
var to_transactions=[86,114,106,106,107,111,133,221,783, 2478];
var ctx = document.getElementById("Chart");
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
                labels: dates,
                datasets: [
                              {
                              data: to_transactions,
                              label: "To Transactions",
                              borderColor: "#3e95cd",
                              fill: false
                              },
                              {
                              data: from_transactions,
                              label: "From Transactions",
                              borderColor: "#ff0000",
                              fill: false
                              },
                ]
          }
});