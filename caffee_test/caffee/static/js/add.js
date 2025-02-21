document.getElementById('add-product').addEventListener('click', function() {
    const productFields = document.getElementById('product-fields');
    const index = productFields.children.length;

    const newField = document.createElement('div');
    newField.className = 'product-field';
    newField.id = `product-field-${index}`;
    newField.innerHTML = `
        <label for="name-${index}">Название блюда:</label>
        <input type="text" name="name-${index}" id="name-${index}" required>
        <label for="price-${index}">Цена:</label>
        <input type="number" name="price-${index}" id="price-${index}" step="0.01" required>
    `;
    productFields.appendChild(newField);
});