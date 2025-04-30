async function convertToFacets(providerId) {
    try {
        const response = await fetch(`/upload_provider/convert_to_facets/${providerId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to convert to Facets');
        }
        
        if (data.success) {
            location.reload();
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
    } catch (err) {
        console.error('Conversion Error:', err);
        alert(`Error converting to Facets: ${err.message}`);
    }
}