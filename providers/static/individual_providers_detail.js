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
        console.error('Full error details:', err.stack);
        alert(`Error converting to Facets: ${err.message}\nCheck browser console for details`);
    }
}