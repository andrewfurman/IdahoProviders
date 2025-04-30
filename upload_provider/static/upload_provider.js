
document.addEventListener('DOMContentLoaded', function() {
  const uploadForm = document.getElementById('uploadForm');
  const processingStatus = document.getElementById('processingStatus');
  const extractionResults = document.getElementById('extractionResults');
  const markdownContent = document.getElementById('markdownContent');

  uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Show processing status
    processingStatus.classList.remove('hidden');
    extractionResults.classList.add('hidden');
    
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
      
      // Create provider record
      const createProviderUrl = uploadForm.dataset.createProviderUrl;
      const providerResponse = await fetch(createProviderUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ markdown_text: markdown })
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
      processingStatus.classList.add('hidden');
    }
  });
});
