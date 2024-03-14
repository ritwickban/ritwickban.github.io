function scrollToContent() {
    const content = document.getElementById('content');
    content.classList.add('visible');
    content.scrollIntoView({ behavior: 'smooth' });
  }
  