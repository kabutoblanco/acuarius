function addAmount(id, price, url, event) {
    event.preventDefault();
    let amount = $("#amount-"+id).val();
    amount++;
    price = parseInt(amount * price);
    price = price.toLocaleString();
    $("#amount-"+id).val(amount);

    updateCart(id, url);
}

function restAmount(id, price, url, event) {
    event.preventDefault();
    let amount = $("#amount-"+id).val();
    let prevAmount = $("#amount-"+id).val();
    amount--;
    amount = amount < 1 ? 1 : amount;
    price = parseInt(amount * price);
    price = price.toLocaleString();
    $("#amount-"+id).val(amount);

    if (prevAmount >= 2) updateCart(id, url);
}

function deleteItem(id, url, event) {
    event.preventDefault();
    updateCart(id, url);
}

function updateCart(id, url) {
    fetch(url, {
        method: 'POST',
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({}),
    }).then((res) => {
        res.json().then((data) => {
            $("#subtotal").text(`$${data["total__sum"].toLocaleString()}`);
            $("#discount").text(`$${data["discount__sum"].toLocaleString()}`);
            $("#total").text(`$${(parseInt(data["total__sum"]) - parseInt(data["discount__sum"])).toLocaleString()}`);
            $("#total-"+id).text(`$${data["total_self"].toLocaleString()}`);

            if (data["type"] == 2) location.href = '/carrito';
        });
    });
}