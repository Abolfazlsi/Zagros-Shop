function rating(slug) {
    var element = document.getElementById("rating")
    var count = document.getElementById("count")
    $.get(`/product/rating/${slug}`).then(response => {
        if (response["response"] === "rating") {
            element.className = "fas fa-star text-warning"
            count.innerText = Number(count.innerText) + 1
        } else {
            element.className = "far fa-star text-warning"
            count.innerText = Number(count.innerText) - 1

        }
    })
}