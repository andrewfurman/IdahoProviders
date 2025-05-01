// ───────────────────────────────────────────────────────────────
//  providers/static/individual_providers_detail.js
//  Handles client‑side actions for the individual provider detail page
// ───────────────────────────────────────────────────────────────

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
  // Buttons
  const extractButton = document.getElementById('extractProviderInfoBtn');
  const convertButton = document.getElementById('convertToFacetsBtn');

  // Provider ID is embedded in the form action URL
  const providerForm = document.getElementById('providerForm');
  let providerId = null;
  if (providerForm) {
    const formAction = providerForm.getAttribute('action');
    providerId = formAction.split('/').pop().split('?')[0];
  }

  // Graceful fallback if providerId could not be parsed
  if (!providerId) {
    console.error('Unable to determine provider_id from providerForm action URL.');
    return;
  }

  // --------------------  Extract Provider Info  --------------------
  if (extractButton) {
    extractButton.addEventListener('click', async () => {
      try {
        const resp = await fetch(`/upload/extract_provider_info/${providerId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });

        const data = await resp.json();
        if (data.success) {
          alert('Provider information extracted successfully');
          window.location.reload();
        } else {
          throw new Error(data.error || 'Unknown error extracting provider info');
        }
      } catch (err) {
        console.error('Error extracting provider info:', err);
        alert(`Error extracting provider information: ${err.message}`);
      }
    });
  }

  // --------------------  Convert to Facets  --------------------
  if (convertButton) {
    convertButton.addEventListener('click', async () => {
      try {
        const resp = await fetch(`/upload/convert_to_facets/${providerId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });

        const data = await resp.json();
        if (data.success) {
          alert('Provider data converted to Facets successfully');
          window.location.reload();
        } else {
          throw new Error(data.error || 'Unknown error converting to Facets');
        }
      } catch (err) {
        console.error('Error converting provider to Facets:', err);
        alert(`Error converting to Facets: ${err.message}`);
      }
    });
  }
});
