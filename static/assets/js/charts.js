
    // Bar Chart - Monthly Orders
    const labels = JSON.parse('{{ month|escapejs }}');
    const data = JSON.parse('{{ orders_count|escapejs }}');

    const barctx = document.getElementById("barChart");
    new Chart(barctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Orders",
                data: data,
                backgroundColor: 'rgba(185, 168, 72, 0.2)',
                borderColor: 'rgba(185, 168, 72, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#F9FAFB'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255,255,255,0.1)'
                    },
                    ticks: {
                        color: '#F9FAFB'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255,255,255,0.1)'
                    },
                    ticks: {
                        color: '#F9FAFB'
                    }
                }
            }
        }
    });
    
    // Pie Chart - Stock Status
    const pieCtx = document.getElementById("pieChart");
    const pieData = JSON.parse('{{ in_out_stock_data|escapejs }}');
    const pieLabels = JSON.parse('{{ in_out_stock_labels|escapejs }}');
    new Chart(pieCtx, {
        type: "pie",
        data: {
            labels: pieLabels,
            datasets: [{
                label: "Stock Status",
                data: pieData,
                backgroundColor: [
                    'rgba(3, 250, 65, 0.84)',
                    'rgba(209, 2, 47, 0.8)',
                ],
                borderColor: [
                    'rgb(7, 200, 0)',
                    'rgb(196, 7, 48)',
                ],
                borderWidth: 1,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#F9FAFB'
                    }
                }
            }
        },
    });
