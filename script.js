document.getElementById('toggle-btn').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('active');
});

document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('file');
    const file = fileInput.files[0];
    if (!file) {
        document.getElementById('result').innerHTML = '<p style="color: #ff4444;">Error: No file selected</p>';
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Network response was not ok');
        }

        // Update Metrics
        const totalPredictions = result.results.length;
        const attackCount = result.results.filter(row => row.Prediction === 'Attack').length;
        const attackPercentage = totalPredictions ? ((attackCount / totalPredictions) * 100).toFixed(1) : 0;
        const accuracy = attackCount > 0 ? '90%' : '95%'; // Placeholder: adjust if backend provides accuracy
        document.getElementById('total-predictions').textContent = totalPredictions;
        document.getElementById('attack-count').textContent = attackCount;
        document.getElementById('accuracy').textContent = accuracy;
        document.querySelector('.attack-change').textContent = `+${attackPercentage}%`;

        // Pie Chart
        const normalCount = totalPredictions - attackCount;
        const pieChart = new Chart(document.getElementById('predictionPieChart'), {
            type: 'pie',
            data: {
                labels: ['Normal', 'Attack'],
                datasets: [{
                    data: [normalCount, attackCount],
                    backgroundColor: ['#00ff00', '#ff4444'],
                    borderColor: '#00f7ff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#e0e0e0',
                            font: { family: 'Fira Code', size: 14 }
                        }
                    },
                    title: {
                        display: true,
                        text: 'Prediction Distribution',
                        color: '#00ff00',
                        font: { family: 'Fira Code', size: 16 }
                    }
                }
            }
        });

        // Bar Chart
        const barChart = new Chart(document.getElementById('probabilityBarChart'), {
            type: 'bar',
            data: {
                labels: result.results.map((_, i) => `Row ${i + 1}`),
                datasets: [{
                    label: 'Attack Probability (%)',
                    data: result.results.map(row => row.Attack_Probability),
                    backgroundColor: result.results.map(row => row.Attack_Probability > 50 ? '#ff4444' : '#00ff00'),
                    borderColor: '#00f7ff',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Probability (%)',
                            color: '#e0e0e0',
                            font: { family: 'Fira Code', size: 14 }
                        },
                        ticks: { color: '#e0e0e0' }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Data Rows',
                            color: '#e0e0e0',
                            font: { family: 'Fira Code', size: 14 }
                        },
                        ticks: { color: '#e0e0e0' }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#e0e0e0',
                            font: { family: 'Fira Code', size: 14 }
                        }
                    }
                }
            }
        });

        // Line Chart (Attack Probability Trend)
        const lineChart = new Chart(document.getElementById('trendLineChart'), {
            type: 'line',
            data: {
                labels: result.results.map(row => row.Timestamp),
                datasets: [{
                    label: 'Attack Probability Trend (%)',
                    data: result.results.map(row => row.Attack_Probability),
                    borderColor: '#00f7ff',
                    backgroundColor: result.results.map(row => row.Prediction === 'Attack' ? '#ff4444' : '#00ff00'),
                    pointBackgroundColor: result.results.map(row => row.Prediction === 'Attack' ? '#ff4444' : '#00ff00'),
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Probability (%)',
                            color: '#e0e0e0',
                            font: { family: 'Fira Code', size: 14 }
                        },
                        ticks: { color: '#e0e0e0' }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Timestamp (s)',
                            color: '#e0e0e0',
                            font: { family: 'Fira Code', size: 14 }
                        },
                        ticks: { color: '#e0e0e0' }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#e0e0e0',
                            font: { family: 'Fira Code', size: 14 }
                        }
                    },
                    title: {
                        display: true,
                        text: 'Attack Probability Trend Over Time',
                        color: '#00ff00',
                        font: { family: 'Fira Code', size: 16 }
                    }
                }
            }
        });

        // Raw Data Table
        let table = `
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>CAN_ID</th>
                    <th>DLC</th>
                    <th>DATA0</th>
                    <th>DATA1</th>
                    <th>DATA2</th>
                    <th>DATA3</th>
                    <th>DATA4</th>
                    <th>DATA5</th>
                    <th>DATA6</th>
                    <th>DATA7</th>
                    <th>Prediction</th>
                    <th>Attack Probability (%)</th>
                </tr>
        `;
        result.results.forEach(row => {
            const predictionClass = row.Prediction === 'Attack' ? 'attack' : 'normal';
            table += `
                <tr>
                    <td>${row.Timestamp}</td>
                    <td>${row.CAN_ID}</td>
                    <td>${row.DLC}</td>
                    <td>${row.DATA0}</td>
                    <td>${row.DATA1}</td>
                    <td>${row.DATA2}</td>
                    <td>${row.DATA3}</td>
                    <td>${row.DATA4}</td>
                    <td>${row.DATA5}</td>
                    <td>${row.DATA6}</td>
                    <td>${row.DATA7}</td>
                    <td class="${predictionClass}">${row.Prediction}</td>
                    <td>${row.Attack_Probability}</td>
                </tr>
            `;
        });
        table += '</table>';
        document.getElementById('rawDataTable').innerHTML = table;

        // Toggle Table
        document.getElementById('toggleTable').addEventListener('click', function() {
            const tableDiv = document.getElementById('rawDataTable');
            tableDiv.style.display = tableDiv.style.display === 'none' ? 'block' : 'none';
            this.textContent = tableDiv.style.display === 'none' ? 'Show Raw Data' : 'Hide Raw Data';
        });

    } catch (error) {
        document.getElementById('result').innerHTML = `<p style="color: #ff4444;">Error: ${error.message}</p>`;
    }
});