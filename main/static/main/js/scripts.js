let button = document.querySelector('button')
let panel = document.querySelector('nav')

button.onclick = function() {
    panel.classList.toggle('opened');
}