$(document).ready(() => {
    $("#amount").val(1);
});

function addDetail(element, id, path) {
    let details = eval(`[${$("#details").val()}]`);
    details.push(id);

    details.forEach(detail => {
        $("#detail-"+detail).find(".check-image-container").addClass("detail-added");
        $("#detail-"+detail).find(".check-image-container").find("img").attr("src", path + "img/check.png");
    });

    details = details.reduce((b, a) => a + "," + b, "");

    $("#details").val(details);
}

function addAmount(price, event) {
    event.preventDefault();
    let amount = $("#amount").val();
    amount++;
    price = parseInt(amount * price );
    price = price.toLocaleString();
    $("#amount").val(amount);
    $("#price").text(`$${price}`);
}

function restAmount(price, event) {
    event.preventDefault();
    let amount = $("#amount").val();
    amount--;
    amount = amount < 1 ? 1 : amount;
    price = parseInt(amount * price );
    price = price.toLocaleString();
    $("#amount").val(amount);
    $("#price").text(`$${price}`);
}

function setColor(element, color) {
    let colorInput = $("#color");
    colorInput.val(color);

    let colorList = $(".color-circle");
    colorList.removeClass("color-circle-activate");
    $(element).addClass("color-circle-activate");
}