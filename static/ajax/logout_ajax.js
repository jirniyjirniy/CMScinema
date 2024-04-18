$(document).ready(function () {
    $('#logout-form').submit(function (e) {
        e.preventDefault()
        window.location.replace('{% url "cinema:index" %}')
    })
})