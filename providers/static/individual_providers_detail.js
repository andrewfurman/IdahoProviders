
async function extractProviderInfo(providerId) {
    try {
        const response = await fetch(`/upload/extract_provider_info/${providerId}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            }
        });
        const data = await response.json();
        if (data.success) {
            location.reload();
        } else {
            alert('Failed to extract provider info: ' + (data.error || 'Unknown error'));
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Error extracting provider info');
    }
}

async function convertToFacets(providerId) {
    try {
        const response = await fetch(`/upload/convert_to_facets/${providerId}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            }
        });
        const data = await response.json();
        if (data.success) {
            location.reload();
        } else {
            alert('Failed to convert to Facets: ' + (data.error || 'Unknown error'));
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Error converting to Facets');
    }
}
