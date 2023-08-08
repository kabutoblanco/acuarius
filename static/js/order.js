function tooglePickup(element, url, event) {
    event.preventDefault();
    let isPickup = $(element).is(':checked');
    updateOrder(isPickup, url);
}

function updateOrder(isPickup, url) {
    fetch(url, {
        method: 'POST',
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({
            isPickup
        }),
    }).then((res) => {
        res.json().then((data) => {
            $("#subtotal").text(`$${data["total__sum"].toLocaleString()}`)
            $("#discount").text(`$${data["discount__sum"].toLocaleString()}`)
            $("#price_sending").text(`$${data["price_sending"].toLocaleString()}`)
            $("#total").text(`$${(parseInt(data["total"])).toLocaleString()}`)
        });
    });
}