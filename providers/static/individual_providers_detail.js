async function convertToFacets(providerId) {
    try {
        const response = await fetch(`/upload_provider/convert_to_facets/${providerId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        console.log('Server response:', data);
        
        if (!response.ok) {
            throw new Error(data.error || data.details || 'Failed to convert to Facets');
        }
        
        if (data.success) {
            location.reload();
        } else {
            throw new Error(data.error || data.details || 'Unknown error occurred');
        }
    } catch (err) {
        console.error('Conversion Error:', err);
        let errorMessage = 'Error converting to Facets';
        if (data && (data.error || data.details)) {
            errorMessage += '\n' + (data.error || '') + '\n' + (data.details || '');
            console.error('Server error details:', data);
        } else {
            console.error('Full error details:', err.stack);
            errorMessage += ': ' + err.message;
        }
        alert(errorMessage);
    }
}