class CupcakeManager {
    constructor() {}

    // Fetch all cupcakes from the API
    static fetchAllCupcakes() {
        return axios.get('/api/cupcakes');
    }

    // Create a new cupcake
    static createCupcake(formData) {
        return axios.post('/api/cupcakes', formData);
    }

    // Update a cupcake by its ID
    updateCupcake(cupcakeId, formData) {
        return axios.patch(`/api/cupcakes/${cupcakeId}`, formData);
    }

    // Delete a cupcake by its ID
    deleteCupcake(cupcakeId) {
        return axios.delete(`/api/cupcakes/${cupcakeId}`);
    }

    // Search for cupcakes using a search term
    searchCupcakes(searchTerm) {
        return axios.get('/api/cupcakes', { params: { search_term: searchTerm } });
    }
}

// Function to render cupcakes on the page
function renderCupcakes(cupcakes) {
    $('#cupcakes-list').empty();
    cupcakes.forEach(function(cupcake) {
        let imageUrl = cupcake.image;
        $('#cupcakes-list').append(`
        <li>${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating} 
        <img src="${imageUrl}" alt="Cupcake Image">
        <a href="/edit/${cupcake.id}" class="update-btn">Edit</a></li>
        `);
    });
}

// Initial call to fetch cupcakes when the page loads
CupcakeManager.fetchAllCupcakes()
    .then(function(response) {
        renderCupcakes(response.data.cupcakes);
    })
    .catch(function(error) {
        console.log('Error fetching cupcakes:', error);
    });

// Event listener for form submission to add new cupcake
$('#new-cupcake-form').submit(function(event) {
    event.preventDefault();
    var formData = {
        flavor: $('#flavor').val(),
        size: $('#size').val(),
        rating: parseFloat($('#rating').val()), // Parse rating as a float
        image: $('#image').val()
    };

    // Validate that the rating is not empty and is a valid numeric value
    if (isNaN(formData.rating)) {
        alert('Please provide a valid rating.');
        return;
    }

    CupcakeManager.createCupcake(formData)
        .then(function(response) {
            renderCupcakes([response.data.cupcake]);
            // Clear form fields
            $('#new-cupcake-form')[0].reset();
        })
        .catch(function(error) {
            console.log('Error adding cupcake:', error);
        });
});

// Event listener for input in the search term field
$('#search-term').on('input', function() {
    let searchTerm = $(this).val().trim();
    const manager = new CupcakeManager(); // Create an instance of CupcakeManager
    manager.searchCupcakes(searchTerm)
        .then(function(response) {
            renderCupcakes(response.data.cupcakes);
        })
        .catch(function(error) {
            console.log('Error fetching cupcakes:', error);
        });
});

function editCupcake(cupcakeId, formData) {
    return axios.patch(`/api/cupcakes/${cupcakeId}`, formData);
}

// Event listener for update button click
$('#cupcakes-list').on('click', '.update-btn', function() {
    let cupcakeId = $(this).data('cupcake-id');
    // Assuming you have a function to fetch cupcake details by ID
    // You need to implement this function to fetch cupcake details
    fetchCupcakeById(cupcakeId)
        .then(function(response) {
            // Populate form fields with cupcake details
            let cupcakeData = response.data.cupcake;
            $('#flavor').val(cupcakeData.flavor);
            $('#size').val(cupcakeData.size);
            $('#rating').val(cupcakeData.rating);
            $('#image').val(cupcakeData.image);
            // Assuming you have a function to show a modal for editing
            // You need to implement this function to display the form
            showModalForEditing(); 
        })
        .catch(function(error) {
            console.log('Error fetching cupcake details:', error);
        });
});

// Event listener for form submission to update cupcake
$('#update-cupcake-form').submit(function(event) {
    event.preventDefault();
    let cupcakeId = $('#cupcake-id').val();
    let formData = {
        flavor: $('#flavor').val(),
        size: $('#size').val(),
        rating: parseFloat($('#rating').val()),
        image: $('#image').val()
    };

    if (isNaN(formData.rating)) {
        alert('Please provide a valid rating.');
        return;
    }

    // Call updateCupcake function with cupcakeId and formData
    editCupcake(cupcakeId, formData)
        .then(function(response) {
            // Edit cupcake in the list
            editCupcakeInList(response.data.cupcake);
            // Close modal or hide form
            closeModalOrHideForm();
        })
        .catch(function(error) {
            console.log('Error updating cupcake:', error);
        });
});