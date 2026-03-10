// Configuração da API (usar mesma origem quando servido pelo backend)
const API_BASE = window.location.origin;

// Form de documentação
const form = document.getElementById('doc-form');
const submitBtn = document.getElementById('submit-btn');
const loading = document.getElementById('doc-loading');
const result = document.getElementById('doc-result');
const docContent = document.getElementById('doc-content');
const screenshotsPath = document.getElementById('screenshots-path');
const errorBox = document.getElementById('doc-error');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const videoInput = document.getElementById('video');
  const vttInput = document.getElementById('vtt');
  
  if (!videoInput.files[0] || !vttInput.files[0]) {
    showError('Selecione o vídeo e o arquivo VTT.');
    return;
  }

  const formData = new FormData();
  formData.append('video', videoInput.files[0]);
  formData.append('vtt', vttInput.files[0]);

  hideError();
  result.style.display = 'none';
  loading.style.display = 'block';
  submitBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/documentation/generate`, {
      method: 'POST',
      body: formData,
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      throw new Error(data.detail || `Erro ${res.status}`);
    }

    let doc = data.documentation || '';
    const screenshots = data.screenshots_base64 || {};
    const filenames = Object.keys(screenshots);

    // Usa placeholders (marked escapa HTML, então injetamos depois)
    const placeholders = [];
    doc = doc.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_, alt, url) => {
      const fn = filenames.find(f => url.includes(f));
      const b64 = fn && screenshots[fn];
      if (b64) {
        const idx = placeholders.length;
        placeholders.push('<img src="data:image/jpeg;base64,' + b64 + '" alt="' + (alt || 'Screenshot').replace(/"/g, '&quot;') + '" style="max-width:100%;display:block;margin:1rem 0;border-radius:8px" />');
        return '\n\n{{IMG' + idx + '}}\n\n';
      }
      return '![' + alt + '](' + url + ')';
    });

    let html = marked.parse(doc);
    placeholders.forEach((imgHtml, idx) => {
      html = html.replace('{{IMG' + idx + '}}', imgHtml);
    });

    docContent.innerHTML = html;

    screenshotsPath.textContent = data.screenshots_folder || 'N/A';
    result.style.display = 'block';
  } catch (err) {
    showError(err.message || 'Erro ao gerar documentação.');
  } finally {
    loading.style.display = 'none';
    submitBtn.disabled = false;
  }
});

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.style.display = 'block';
}

function hideError() {
  errorBox.style.display = 'none';
  errorBox.textContent = '';
}
