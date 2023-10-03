BASE_URL = 'http://127.0.0.1:5000/api';


function generateCupcakeHTML(cupcake) {
    return `<div data-cupcake-id=${cupcake.id} class="mb-4">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                    <button class="delete-button">X</button>
                </li>
                <img class="img-fluid" src="${cupcake.image}" alt="(no image provided)">
            </div>`;
}


async function showInitialCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for(let cupcakeData of response.data.cupcakes){
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $('#cupcake-list').append(newCupcake);
    }
}


$('#cupcake-form').on('submit', async function(e){
    e.preventDefault();

    let flavor = $("#flavor").val();
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("#image").val();

    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $('#cupcake-list').append(newCupcake);
    $('#cupcake-form').trigger('reset');
});


$('#cupcake-list').on('click', '.delete-button', async function(e){
    e.preventDefault();
    let $cupcake = $(e.target).closest('div');
    let cupcakeId = $cupcake.attr('data-cupcake-id')

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});


$(showInitialCupcakes);