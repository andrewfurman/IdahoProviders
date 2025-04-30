
async function convertToFacets(providerId) {
    try {
        const response = await fetch(`/upload/convert_to_facets/${providerId}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        const data = await response.json();
        console.log('Server response:', data);
        
        if (!response.ok) {
            let errorMsg = 'Failed to convert to Facets\n\n';
            if (data.error) errorMsg += `Error: ${data.error}\n`;
            if (data.details) errorMsg += `Details: ${data.details}`;
            alert(errorMsg);
            return;
        }
        
        if (data.success) {
            location.reload();
        } else {
            alert(data.error || data.details || 'Unknown error occurred');
        }
    } catch (err) {
        console.error('Conversion Error:', err);
        console.error('Error stack:', err.stack);
        alert(`Error converting to Facets: ${err.message}`);
    }
}

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
            alert('Failed to extract provider info');
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Error extracting provider info');
    }
}
