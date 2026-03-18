// API Base URL - using relative path for deployment
const API_URL = '/api';

const uploadZone = document.getElementById('upload-zone');
const processingZone = document.getElementById('processing-zone');
const resultZone = document.getElementById('result-zone');
const errorZone = document.getElementById('error-zone');

const fileInput = document.getElementById('file-input');
const progressFill = document.getElementById('progress-fill');
const loaderText = document.querySelector('.loader-text');
const downloadBtn = document.getElementById('download-btn');
const pageCount = document.getElementById('page-count');
const errorMessage = document.getElementById('error-message');

// Drag Events
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evtName => {
    uploadZone.addEventListener(evtName, (e) => e.preventDefault());
});

['dragenter', 'dragover'].forEach(evtName => {
    uploadZone.addEventListener(evtName, () => uploadZone.classList.add('dragover'));
});

['dragleave', 'drop'].forEach(evtName => {
    uploadZone.addEventListener(evtName, () => uploadZone.classList.remove('dragover'));
});

uploadZone.addEventListener('drop', (e) => {
    const file = e.dataTransfer.files[0];
    handleFile(file);
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFile(file);
});

// Reset logic
document.getElementById('reset-btn').addEventListener('click', resetView);
document.getElementById('retry-btn').addEventListener('click', resetView);

function resetView() {
    fileInput.value = '';
    resultZone.classList.add('hidden');
    errorZone.classList.add('hidden');
    uploadZone.classList.remove('hidden');
}

function showProcessing() {
    uploadZone.classList.add('hidden');
    errorZone.classList.add('hidden');
    processingZone.classList.remove('hidden');
    progressFill.style.width = '0%';
}

function showSuccess(data) {
    processingZone.classList.add('hidden');
    resultZone.classList.remove('hidden');
    pageCount.innerText = `Limpamos o seu PDF removendo as marcas (${data.pages_processed || 0} páginas processadas).`;
    downloadBtn.href = `${API_URL}/download/${data.task_id}`;
    downloadBtn.download = data.filename;
}

function showError(msg) {
    processingZone.classList.add('hidden');
    errorZone.classList.remove('hidden');
    errorMessage.innerText = msg;
}

async function handleFile(file) {
    if (!file) return;

    if (file.type !== 'application/pdf') {
        alert('Por favor, selecione apenas arquivos PDF.');
        return;
    }

    if (file.size > 50 * 1024 * 1024) {
        alert('Tamanho limite de 50MB excedido.');
        return;
    }

    showProcessing();

    const formData = new FormData();
    formData.append('file', file);

    try {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', `${API_URL}/remove-watermark`, true);

        // Upload progress
        xhr.upload.onprogress = (e) => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 50);
                progressFill.style.width = percent + '%';
                loaderText.innerText = `Enviando... ${percent}%`;
            }
        };

        xhr.onload = () => {
            if (xhr.status === 200) {
                progressFill.style.width = '100%';
                loaderText.innerText = `Concluído!`;

                try {
                    const data = JSON.parse(xhr.responseText);
                    setTimeout(() => showSuccess(data), 500);
                } catch (e) {
                    showError("Formato de resposta inválido.");
                }
            } else {
                let errData;
                try {
                    errData = JSON.parse(xhr.responseText);
                    showError(errData.detail || 'Erro ao processar arquivo.');
                } catch {
                    showError('Erro ao processar arquivo.');
                }
            }
        };

        xhr.onerror = () => {
            showError("Erro na conexão com o servidor. Verifique se a API está rodando.");
        };

        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                // Done
            } else if (xhr.readyState === XMLHttpRequest.HEADERS_RECEIVED) {
                progressFill.style.width = '75%';
                loaderText.innerText = 'Processando páginas... isso pode levar p/ alguns segundos';
            }
        };

        xhr.send(formData);

    } catch (err) {
        showError("Ocorreu um erro inesperado.");
        console.error(err);
    }
}
