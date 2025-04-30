
document.addEventListener('DOMContentLoaded', function() {
  const uploadForm = document.getElementById('uploadForm');
  const processingStatus = document.getElementById('processingStatus');
  const extractionResults = document.getElementById('extractionResults');
  const markdownContent = document.getElementById('markdownContent');
  let processingTimer;
  let processingSeconds = 0;

  uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Show processing status and start timer
    processingStatus.classList.remove('hidden');
    extractionResults.classList.add('hidden');
    processingSeconds = 0;
    
    const statusText = processingStatus.querySelector('p');
    processingTimer = setInterval(() => {
      processingSeconds++;
      statusText.textContent = `Processing image... (${processingSeconds} second${processingSeconds !== 1 ? 's' : ''})`;
    }, 1000);
    
    try {
      // First process the image
      const formData = new FormData(uploadForm);
      const response = await fetch(uploadForm.action, {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) throw new Error('Image processing failed');
      
      const { markdown } = await response.json();
      
      // Show extraction results
      markdownContent.innerHTML = marked.parse(markdown);
      extractionResults.classList.remove('hidden');
      
      // Create provider record with both markdown and image
      const createProviderUrl = uploadForm.dataset.createProviderUrl;
      const formData = new FormData();
      formData.append('markdown_text', markdown);
      formData.append('image_file', document.querySelector('input[name="image_file"]').files[0]);
      
      const providerResponse = await fetch(createProviderUrl, {
        method: 'POST',
        body: formData
      });
      
      if (!providerResponse.ok) {
        const errorData = await providerResponse.text();
        console.error('Provider creation failed:', errorData);
        throw new Error(`Provider creation failed: ${errorData}`);
      }
      
      const { provider_id } = await providerResponse.json();
      
      // Wait 5 seconds then redirect
      await new Promise(resolve => setTimeout(resolve, 5000));
      
      // Redirect to provider detail page
      const detailUrl = uploadForm.dataset.providerDetailUrl.replace('/0', `/${provider_id}`);
      window.location.href = detailUrl;
      
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while processing the request');
    } finally {
      clearInterval(processingTimer);
      processingStatus.classList.add('hidden');
    }
  });
});
