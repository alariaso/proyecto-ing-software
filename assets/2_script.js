document.documentElement.setAttribute('data-bs-theme', 'dark')

function savePDF() {
    const body = document.getElementsByTagName("body")[0]
    html2pdf(body, {filename: 'informe.pdf'})
}
