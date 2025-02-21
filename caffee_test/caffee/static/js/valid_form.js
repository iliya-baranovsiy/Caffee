import { post } from "./post.js";

document.getElementById('product-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {
        table_number: formData.get('table'),
        items: {},
        total_price: 0,
        status: "в ожидании"
    };

    const productFields = document.querySelectorAll('.product-field');
    let hasError = false;

    productFields.forEach((field, index) => {
        const name = formData.get(`name-${index}`);
        const price = parseFloat(formData.get(`price-${index}`));

        if (!isNaN(name) && name.trim() !== '') {
            hasError = true;
            window.alert("Ошибка: Название блюда не должно содержать только числа.")
        } else if (name && !isNaN(price)) {
            data.items[name] = price;
            data.total_price += price;
        }
    });

    if (hasError) {
        return;
    }

    function clearForm() {
        document.getElementById("product-form").reset();
    }

    post(data).then(() => {
        location.reload();
    });

    clearForm();
});