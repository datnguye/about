/**
 * Stacked Bar Chart Module
 * Creates reusable stacked bar charts for visualizing prompt structures
 */

class StackedBarChart {
  constructor(container, options = {}) {
    this.container = typeof container === 'string' ? document.querySelector(container) : container;
    this.options = {
      height: options.height || 300,
      minWidth: options.minWidth || 300,
      maxWidth: options.maxWidth || 400,
      showCaption: options.showCaption !== false,
      captionText: options.captionText || '',
      ...options
    };
  }

  /**
   * Create a stacked bar chart
   * @param {Array} items - Array of objects with { label, color, textColor, emoji }
   * @returns {HTMLElement} The created chart element
   */
  create(items) {
    if (!this.container) {
      console.error('Container element not found');
      return null;
    }

    // Clear existing content
    this.container.innerHTML = '';

    // Create wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'stacked-bar-wrapper';

    // Create chart container
    const chartContainer = document.createElement('div');
    chartContainer.className = 'stacked-bar-container';
    chartContainer.style.minWidth = `${this.options.minWidth}px`;
    chartContainer.style.maxWidth = `${this.options.maxWidth}px`;

    // Create chart
    const chart = document.createElement('div');
    chart.className = 'stacked-bar-chart';
    chart.style.height = `${this.options.height}px`;

    // Create bars
    items.forEach((item, index) => {
      const bar = document.createElement('div');
      bar.className = 'stacked-bar-item';
      bar.style.background = item.color;
      bar.style.flex = '1';
      
      if (index < items.length - 1) {
        bar.style.borderBottom = '1px solid #ddd';
      }

      const label = document.createElement('span');
      label.className = 'stacked-bar-label';
      label.style.color = item.textColor || '#000';
      label.innerHTML = `${item.label} ${item.emoji || ''}`;

      bar.appendChild(label);
      chart.appendChild(bar);
    });

    chartContainer.appendChild(chart);
    wrapper.appendChild(chartContainer);

    // Add caption if needed
    if (this.options.showCaption && this.options.captionText) {
      const caption = document.createElement('p');
      caption.className = 'stacked-bar-caption';
      caption.innerHTML = `<em>${this.options.captionText}</em>`;
      wrapper.appendChild(caption);
    }

    this.container.appendChild(wrapper);
    return wrapper;
  }

  /**
   * Create a comparison view with two charts side by side
   * @param {Object} chart1 - { title, items }
   * @param {Object} chart2 - { title, items }
   * @returns {HTMLElement} The created comparison element
   */
  createComparison(chart1, chart2) {
    if (!this.container) {
      console.error('Container element not found');
      return null;
    }

    // Clear existing content
    this.container.innerHTML = '';

    // Create main wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'stacked-bar-comparison';

    // Create chart 1
    const container1 = document.createElement('div');
    container1.className = 'stacked-bar-comparison-item';
    
    if (chart1.title) {
      const title1 = document.createElement('h4');
      title1.className = 'stacked-bar-title';
      title1.textContent = chart1.title;
      container1.appendChild(title1);
    }

    const chartWrapper1 = document.createElement('div');
    chartWrapper1.className = 'stacked-bar-container';
    chartWrapper1.style.minWidth = `${this.options.minWidth}px`;
    chartWrapper1.style.maxWidth = `${this.options.maxWidth}px`;

    const chartEl1 = this._createChart(chart1.items);
    chartWrapper1.appendChild(chartEl1);
    container1.appendChild(chartWrapper1);

    // Create arrow
    const arrow = document.createElement('div');
    arrow.className = 'stacked-bar-arrow';
    arrow.textContent = '→';

    // Create chart 2
    const container2 = document.createElement('div');
    container2.className = 'stacked-bar-comparison-item';
    
    if (chart2.title) {
      const title2 = document.createElement('h4');
      title2.className = 'stacked-bar-title';
      title2.textContent = chart2.title;
      container2.appendChild(title2);
    }

    const chartWrapper2 = document.createElement('div');
    chartWrapper2.className = 'stacked-bar-container';
    chartWrapper2.style.minWidth = `${this.options.minWidth}px`;
    chartWrapper2.style.maxWidth = `${this.options.maxWidth}px`;

    const chartEl2 = this._createChart(chart2.items);
    chartWrapper2.appendChild(chartEl2);
    container2.appendChild(chartWrapper2);

    // Assemble comparison
    wrapper.appendChild(container1);
    wrapper.appendChild(arrow);
    wrapper.appendChild(container2);

    // Add caption if needed
    if (this.options.showCaption && this.options.captionText) {
      const caption = document.createElement('p');
      caption.className = 'stacked-bar-caption';
      caption.innerHTML = `<em>${this.options.captionText}</em>`;
      wrapper.appendChild(caption);
    }

    this.container.appendChild(wrapper);
    return wrapper;
  }

  /**
   * Internal method to create just the chart element
   */
  _createChart(items) {
    const chart = document.createElement('div');
    chart.className = 'stacked-bar-chart';
    chart.style.height = `${this.options.height}px`;

    items.forEach((item, index) => {
      const bar = document.createElement('div');
      bar.className = 'stacked-bar-item';
      bar.style.background = item.color;
      bar.style.flex = '1';
      
      if (index < items.length - 1) {
        bar.style.borderBottom = '1px solid #ddd';
      }

      const label = document.createElement('span');
      label.className = 'stacked-bar-label';
      label.style.color = item.textColor || '#000';
      label.innerHTML = `${item.label} ${item.emoji || ''}`;

      bar.appendChild(label);
      chart.appendChild(bar);
    });

    return chart;
  }
}

// Auto-initialize charts with data attributes
document.addEventListener('DOMContentLoaded', () => {
  const autoCharts = document.querySelectorAll('[data-stacked-chart]');
  
  autoCharts.forEach(container => {
    try {
      const data = JSON.parse(container.getAttribute('data-stacked-chart'));
      const options = JSON.parse(container.getAttribute('data-chart-options') || '{}');
      
      const chart = new StackedBarChart(container, options);
      
      if (data.comparison) {
        chart.createComparison(data.chart1, data.chart2);
      } else {
        chart.create(data.items);
      }
    } catch (e) {
      console.error('Failed to initialize stacked chart:', e);
    }
  });
});

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
  module.exports = StackedBarChart;
}