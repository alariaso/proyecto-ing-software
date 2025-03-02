document.documentElement.setAttribute("data-bs-theme", "dark")

function savePDF() {
    const body = document.getElementsByTagName("body")[0]
    const opts = {
        filename: "informe.pdf",
        jsPDF: {
            orientation: "landscape",
        }
    }
    html2pdf(body, opts)
}
