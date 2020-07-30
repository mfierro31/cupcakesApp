$(async function(){
  const url = '/api/cupcakes'

  $('ul').empty()

  await getAllCupcakes();

  async function getAllCupcakes() {
    const resp = await axios.get(url);

    for (const cupcake of resp.data.cupcakes) {
      $('ul').append(`
      <li>
        <div class="row mb-5">
          <div class="col-8">
            <p>Flavor: ${cupcake.flavor}</p>
            <p>Size: ${cupcake.size}</p>
            <p>Rating: ${cupcake.rating}</p>
          </div>
          <div class="col-4 text-center">
            <img src="${cupcake.image}" class="img-fluid" alt="${cupcake.flavor} cupcake">
          </div>
        </div>
      </li>`)
    }
  }

  $('form').on('submit', async function(evt) {
    evt.preventDefault();
    const flavor = $('#flavor').val();
    const size = $('#size').val();
    let rating = $('#rating').val();
    rating = parseFloat(rating);
    const image = $('#image').val();

    const data = {
      flavor,
      size,
      rating,
      image
    };

    const resp = await axios.post(url, data);

    const newCupcake = resp.data.cupcake;

    $('ul').append(`
    <li>
        <div class="row mb-5">
          <div class="col-8">
            <p>Flavor: ${newCupcake.flavor}</p>
            <p>Size: ${newCupcake.size}</p>
            <p>Rating: ${newCupcake.rating}</p>
          </div>
          <div class="col-4 text-center">
            <img src="${newCupcake.image}" class="img-fluid" alt="${newCupcake.flavor} cupcake">
          </div>
        </div>
      </li>
    `)
  })

  $('#flavor').val('');
  $('#size').val('');
  $('#rating').val('');
  $('#image').val('');
})