document.addEventListener('DOMContentLoaded', () => {
  const toggleButton = document.getElementById('toggleExperience');
  const olderExperience = document.getElementById('olderExperience');
  const buttonIcon = toggleButton.querySelector('i');
  const buttonText = toggleButton.querySelector('span');
  
  // Initialize state - collapsed by default
  let isExpanded = false;
  
  toggleButton.addEventListener('click', () => {
    isExpanded = !isExpanded;
    
    if (isExpanded) {
      // Expand
      olderExperience.style.maxHeight = olderExperience.scrollHeight + 'px';
      buttonIcon.classList.remove('fa-chevron-down');
      buttonIcon.classList.add('fa-chevron-up');
      buttonText.textContent = 'Show Less';
    } else {
      // Collapse
      olderExperience.style.maxHeight = '0';
      buttonIcon.classList.remove('fa-chevron-up');
      buttonIcon.classList.add('fa-chevron-down');
      buttonText.textContent = 'Show More';
    }
  });
  
  // Initialize collapsed state
  olderExperience.style.maxHeight = '0';
  buttonIcon.classList.remove('fa-chevron-up');
  buttonIcon.classList.add('fa-chevron-down');
  buttonText.textContent = 'Show More';
});