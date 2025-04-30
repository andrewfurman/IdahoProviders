async function convertToFacets(providerId) {
    try {
        const response = await fetch(`/upload/convert_to_facets/${providerId}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Failed to convert to Facets');
        }
        
        location.reload();
    } catch (err) {
        console.error('Error:', err);
        alert('Error converting to Facets');
    }
}