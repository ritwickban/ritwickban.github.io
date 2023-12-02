document.addEventListener('DOMContentLoaded', function () {
    typeOutSubtitle();
});

function typeOutSubtitle() {
    const subtitle = document.querySelector('header p');
    const text = subtitle.innerText;

    subtitle.innerHTML = ''; // Clear the existing text

    for (let i = 0; i < text.length; i++) {
        const charSpan = document.createElement('span');
        charSpan.innerHTML = text.charAt(i);
        subtitle.appendChild(charSpan);

        charSpan.style.animationDelay = `${i * 100}ms`;
    }
}