$(document).ready(() => {
    getBanks('/bancos');
});

function getBanks(url) {
    fetch(url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
        },
    }).then((res) => {
        res.json().then((data) => {
            let bank = $('#bank');
            data.data.forEach((item) => {
                bank.append(
                    $('<option>', {
                        value: item.bankCode,
                        text: item.bankName.replace(/\\u([\d\w]{4})/gi, function (match, grp) {
                            return String.fromCharCode(parseInt(grp, 16));
                        }),
                    })
                );
            });
        });
    });
}
