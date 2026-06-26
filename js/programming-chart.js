document.addEventListener('DOMContentLoaded', () => {
  // Initialize Programming Languages Radar Chart
  const radarCtx = document.getElementById('programmingRadarChart');
  if (radarCtx && window.skillsData && window.skillsData.programming) {
    const data = window.skillsData.programming;
    
    new Chart(radarCtx, {
      type: 'radar',
      data: {
        labels: data.map(lang => lang.name),
        datasets: [{
          label: 'Level',
          data: data.map(lang => lang.level * 10), // Convert to percentage
          borderColor: '#ffffff',
          backgroundColor: 'rgba(255, 255, 255, 0.2)',
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#1a1a1a',
          pointHoverBackgroundColor: '#ffffff',
          pointHoverBorderColor: '#ffffff'
        }, {
          label: 'Preference',
          data: data.map(lang => lang.preference * 10), // Convert to percentage
          borderColor: '#991b1b',
          backgroundColor: 'rgba(153, 27, 27, 0.2)',
          pointBackgroundColor: '#991b1b',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#991b1b'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          r: {
            angleLines: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            pointLabels: {
              color: '#e5e5e5',
              font: {
                size: 11
              }
            },
            ticks: {
              color: '#e5e5e5',
              backdropColor: 'transparent',
              stepSize: 20,
              display: false
            },
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  }
});