// Initialize websocket connection
const socket = io();

// Chart initialization
let performanceChart;

function initializeChart() {
    const ctx = document.getElementById('performance-chart').getContext('2d');
    performanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Portfolio Value',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Strategy Performance'
                }
            }
        }
    });
}

// Update dashboard data
function updateDashboard() {
    fetch('/api/strategy_performance')
        .then(response => response.json())
        .then(data => {
            // Update metrics
            document.getElementById('total-return').textContent = 
                `${(data.total_return * 100).toFixed(2)}%`;
            document.getElementById('sharpe-ratio').textContent = 
                data.sharpe_ratio.toFixed(2);
            document.getElementById('max-drawdown').textContent = 
                `${(data.max_drawdown * 100).toFixed(2)}%`;
            document.getElementById('win-rate').textContent = 
                `${(data.win_rate * 100).toFixed(2)}%`;
            
            // Update chart
            updateChart(data.equity_curve);
            
            // Update positions table
            updatePositionsTable(data.current_positions);
        });
}

function updateChart(equityCurve) {
    performanceChart.data.labels = equityCurve.dates;
    performanceChart.data.datasets[0].data = equityCurve.values;
    performanceChart.update();
}

function updatePositionsTable(</antArtifact>
