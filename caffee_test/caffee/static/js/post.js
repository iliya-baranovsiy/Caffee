function post(data) {
    const data_to_send = data;
    return fetch('api/caffe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .catch(error => console.error('Ошибка:', error));
}

export { post };