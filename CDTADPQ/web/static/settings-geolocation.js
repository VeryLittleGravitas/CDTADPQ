function zip_code_list(original_zipcodes_str, new_zipcode)
{
    var output_zipcodes = [],
        input_zipcodes = original_zipcodes_str.split(',');
    
    for (var i in input_zipcodes)
    {
        output_zipcodes.push(input_zipcodes[i].trim());
    }
    
    if(output_zipcodes.indexOf(new_zipcode) == -1)
    {
        output_zipcodes.push(new_zipcode);
    }
    
    return output_zipcodes.join(', ');
}

function on_geolocation(position, original_zipcodes_str, zipcode_url)
{
    var input = document.getElementById('zip-codes'),
        lat = position.coords.latitude,
        lon = position.coords.longitude;

    input.value = '';
    input.placeholder = 'Finding zip code...';

    var xhr = new XMLHttpRequest(),
        url = zipcode_url + "?lat=" + encodeURIComponent(lat) + "&lon=" + encodeURIComponent(lon);

    xhr.onreadystatechange = function()
    {
        var DONE = this.DONE || 4;
        if (this.readyState === DONE){
            var response = JSON.parse(this.responseText);

            if('zipcode' in response) {
                input.value = zip_code_list(original_zipcodes_str, response['zipcode']);
                input.placeholder = '';
            } else {
                input.value = '';
                input.placeholder = '';
            }
        }
    }

    xhr.open('GET', url, true);
    xhr.send(null);
}
