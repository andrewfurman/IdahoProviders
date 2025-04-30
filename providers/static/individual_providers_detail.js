
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
