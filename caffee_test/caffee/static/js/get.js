function get(table_num) {
    return fetch('api/caffe/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(result => {
        let flag = false;
        for (let i = 0; i < result.length; i++) {
            if (table_num == result[i]['table_number']) {
                flag = true;
                break;
            }
        }
        return flag;
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return false;
    });
}

export { get };