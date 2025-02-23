import { post } from "./post.js";
import { get } from "./get.js";

async function valid() {
    document.getElementById('product-form').addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(this);
        const data = {
            table_number: formData.get('table'),
            items: {},
            total_price: 0,
            status: "в ожидании"
        };

        const isTableOccupied = await get(formData.get('table'));
        if (isTableOccupied) {
            window.alert('Стол с таким номером уже занят');
            return;
        }

        const productFields = document.querySelectorAll('.product-field');
        let hasError = false;

        productFields.forEach((field, index) => {
            const name = formData.get(`name-${index}`);
            const price = parseFloat(formData.get(`price-${index}`));

            if (!isNaN(name) && name.trim() !== '') {
                hasError = true;
                window.alert("Ошибка: Название блюда не должно содержать только числа.");
            } else if (name && !isNaN(price) && price >= 0) {
                data.items[name] = price;
                data.total_price += price;
            } else {
                hasError = true;
                window.alert("Цена не может быть отрицательной");
            }
        });

        if (hasError) {
            return;
        }

        function clearForm() {
            document.getElementById("product-form").reset();
        }

        await post(data);
        clearForm();
        location.reload();
    });
}

valid();