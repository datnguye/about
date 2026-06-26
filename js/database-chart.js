document.addEventListener('DOMContentLoaded', () => {
  // Initialize Database Bar Chart
  const barCtx = document.getElementById('databaseBarChart');
  if (barCtx && window.skillsData && window.skillsData.databases) {
    const data = window.skillsData.databases;
    
    new Chart(barCtx, {
      type: 'bar',
      data: {
        labels: data.map(db => db.name),
        datasets: [{
          label: 'Proficiency',
          data: data.map(db => db.percentage),
          backgroundColor: [
            'rgba(153, 27, 27, 0.8)',
            'rgba(153, 27, 27, 0.7)',
            'rgba(153, 27, 27, 0.6)',
            'rgba(153, 27, 27, 0.5)',
            'rgba(153, 27, 27, 0.4)'
          ],
          borderColor: '#991b1b',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.parsed.x + '%';
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            max: 100,
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            ticks: {
              color: '#e5e5e5',
              callback: function(value) {
                return value + '%';
              }
            }
          },
          y: {
            grid: {
              display: false
            },
            ticks: {
              color: '#e5e5e5',
              font: {
                size: 11
              }
            }
          }
        }
      }
    });
  }
});