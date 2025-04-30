
document.addEventListener('DOMContentLoaded', function() {
  const uploadForm = document.querySelector('form');
  const submitButton = uploadForm.querySelector('button[type="submit"]');
  let elapsedTime = 0;
  let timerInterval;

  function showLoading() {
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

  uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    showLoading();

    const formData = new FormData(this);
    try {
      const response = await fetch(this.action, {
        method: 'POST',
        body: formData
      });
      
      const html = await response.text();
      
      // Extract the markdown content div from response
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const markdownContent = doc.getElementById('markdown-content');
      
      if (markdownContent) {
        // Update just the markdown section
        const currentMarkdownContent = document.getElementById('markdown-content');
        if (currentMarkdownContent) {
          const markdown = markdownContent.getAttribute('data-markdown');
          if (markdown) {
            currentMarkdownContent.setAttribute('data-markdown', markdown);
            currentMarkdownContent.querySelector('#markdown-rendered').innerHTML = marked.parse(markdown);
          }
        } else {
          // If first time, create the results section
          const resultsDiv = document.createElement('div');
          resultsDiv.className = 'mt-10';
          resultsDiv.innerHTML = `
            <h2 class="text-xl font-semibold mb-2">🔤 Extracted Text</h2>
            <div id="markdown-content" class="prose max-w-none bg-gray-50 border rounded p-4 overflow-x-auto">
              <div id="markdown-rendered"></div>
            </div>
          `;
          uploadForm.parentNode.appendChild(resultsDiv);
          
          const markdown = markdownContent.getAttribute('data-markdown');
          if (markdown) {
            resultsDiv.querySelector('#markdown-content').setAttribute('data-markdown', markdown);
            resultsDiv.querySelector('#markdown-rendered').innerHTML = marked.parse(markdown);
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      hideLoading();
    }
  });
});
