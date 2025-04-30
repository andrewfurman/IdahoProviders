
document.addEventListener('DOMContentLoaded', function() {
  const uploadForm = document.querySelector('form');
  const submitButton = uploadForm.querySelector('button[type="submit"]');
  let elapsedTime = 0;
  let timerInterval;

  function showLoading() {
    const originalText = submitButton.innerHTML;
    submitButton.disabled = true;
    
    // Create loading container
    const loadingContainer = document.createElement('div');
    loadingContainer.id = 'loadingContainer';
    loadingContainer.className = 'mt-4 text-center';
    loadingContainer.innerHTML = `
      <div class="animate-spin inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full"></div>
      <div id="timer" class="mt-2 text-gray-600">Waiting: 0s</div>
    `;
    
    // Insert after form
    uploadForm.parentNode.insertBefore(loadingContainer, uploadForm.nextSibling);
    
    // Start timer
    timerInterval = setInterval(() => {
      elapsedTime++;
      document.getElementById('timer').textContent = `Waiting: ${elapsedTime}s`;
    }, 1000);
  }

  function hideLoading() {
    submitButton.disabled = false;
    const loadingContainer = document.getElementById('loadingContainer');
    if (loadingContainer) {
      loadingContainer.remove();
    }
    clearInterval(timerInterval);
    elapsedTime = 0;
  }

  uploadForm.addEventListener('submit', function() {
    showLoading();
  });

  // Handle response completion
  const originalFetch = window.fetch;
  window.fetch = function() {
    return originalFetch.apply(this, arguments)
      .then(response => {
        hideLoading();
        return response;
      })
      .catch(error => {
        hideLoading();
        throw error;
      });
  };
});
