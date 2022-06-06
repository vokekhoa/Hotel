function addToCart(id, name, price) {
    event.preventDefault()
    fetch('/api/add-cart', {
        method: 'post',
        body: {
            'id': id,
            'name': name,
            'price': price
        },
        headers: {
            'Content'
        }
    })
}