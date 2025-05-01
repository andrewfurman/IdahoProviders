
// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
  // Get the Extract Provider Info button
  const extractButton = document.querySelector('button[class*="bg-purple-600"]:first-of-type');
  
  if (extractButton) {
    extractButton.addEventListener('click', async function() {
      try {
        // Get provider ID from the form action URL
        const providerForm = document.getElementById('providerForm');
        const formAction = providerForm.getAttribute('action');
        const providerId = formAction.split('/').pop().split('?')[0];
        
        // Call the extract provider info endpoint
        const response = await fetch(`/upload/extract_provider_info/${providerId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        const data = await response.json();
        
        if (data.success) {
          // Show success message
          alert('Provider information extracted successfully');
          // Refresh the page to show updated information
          window.location.reload();
        } else {
          throw new Error(data.error || 'Failed to extract provider information');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Error extracting provider information: ' + error.message);
      }
    });
  }
});
