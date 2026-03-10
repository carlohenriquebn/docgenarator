"""
Serviço de geração de documentação a partir de vídeo + transcrição VTT.
Extrai frames do vídeo, parseia a transcrição e gera documentação via OpenAI.
"""
import os
import tempfile
import base64
import re
from pathlib import Path
from openai import OpenAI


# Pasta para salvar screenshots (POC)
DOCS_SCREENSHOTS_DIR = Path(__file__).parent / "documentation_screenshots"
DOCS_SCREENSHOTS_DIR.mkdir(exist_ok=True)


def parse_vtt(content: str) -> str:
    """Extrai o texto das legendas VTT. Usa webvtt-py se disponível, senão parse manual."""
    try:
        import webvtt
        vtt = webvtt.WebVTT.from_string(content)
        return " ".join(caption.text for caption in vtt)
    except (ImportError, Exception):
        pass
    # Fallback: parse manual
    lines = content.strip().split("\n")
    texts = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("WEBVTT") or "--> " in line:
            continue
        if "-->" in line:
            continue
        if line and not re.match(r"^\d+$", line):
            texts.append(line)
    return " ".join(texts)


def extract_frames_from_video(video_path: str, output_dir: Path, interval_sec: float = 5.0, max_frames: int = 10) -> list[str]:
    """
    Extrai frames do vídeo em intervalos regulares.
    Retorna lista de caminhos das imagens salvas.
    """
    try:
        import cv2
    except ImportError:
        raise ImportError("opencv-python é necessário. Execute: pip install opencv-python")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Não foi possível abrir o vídeo: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(fps * interval_sec)
    saved_paths: list[str] = []
    frame_idx = 0

    while frame_idx < total_frames and len(saved_paths) < max_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        filename = f"frame_{len(saved_paths):04d}.jpg"
        filepath = output_dir / filename
        cv2.imwrite(str(filepath), frame)
        saved_paths.append(str(filepath))
        frame_idx += frame_interval

    cap.release()
    return saved_paths


def image_to_base64(path: str) -> str:
    """Converte imagem para base64 para envio à API Vision."""
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def generate_documentation(
    transcription_text: str,
    image_paths: list[str],
    openai_client: OpenAI,
    model: str = "gpt-4o",
) -> str:
    """
    Gera documentação estruturada usando transcrição e capturas de tela.
    Usa GPT-4 Vision para analisar as imagens.
    """
    content_parts: list[dict] = [
        {
            "type": "text",
            "text": f"""Você é um redator técnico especializado em criar documentação clara e bem estruturada.

Com base na transcrição do vídeo e nas capturas de tela fornecidas, gere uma documentação completa em Markdown.

## Transcrição do vídeo:
{transcription_text}

## Sua tarefa:
1. Analise as capturas de tela na ordem em que aparecem (representam momentos-chave do vídeo)
2. Crie uma documentação técnica/educacional que combine o que foi dito na transcrição com o que é mostrado visualmente
3. Inclua as imagens na documentação referenciando-as no contexto apropriado. Use: ![Descrição](/documentation/screenshots/frame_0000.jpg) — troque o número para cada imagem (frame_0000, frame_0001, etc.)
4. Estruture com:
   - Título principal
   - Sumário/Índice
   - Seções numeradas com subtítulos claros
   - Listas e bullet points quando apropriado
   - Notas ou dicas importantes destacadas
   - Conclusão ou resumo

Para as imagens, use o caminho: /documentation/screenshots/frame_0000.jpg, /documentation/screenshots/frame_0001.jpg, etc. (uma para cada captura na ordem).

Gere APENAS o conteúdo Markdown da documentação, sem explicações adicionais antes ou depois."""
        }
    ]

    for path in image_paths:
        b64 = image_to_base64(path)
        fname = os.path.basename(path)
        content_parts.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
        })

    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content_parts}],
        max_tokens=4096,
    )
    return response.choices[0].message.content or ""


def get_screenshots_base64(image_paths: list[str]) -> dict[str, str]:
    """Retorna mapa filename -> base64 das imagens."""
    return {os.path.basename(p): image_to_base64(p) for p in image_paths}


def process_video_and_generate_docs(
    video_path: str,
    vtt_content: str,
    openai_client: OpenAI,
    output_dir: Path | None = None,
    interval_sec: float = 5.0,
    max_frames: int = 10,
) -> dict:
    """
    Pipeline completo: extrai frames, parseia VTT e gera documentação.
    Retorna: { "documentation": str, "screenshots": list[str], "transcription": str }
    Inclui screenshots_base64 para o frontend exibir as imagens inline.
    """
    out_dir = output_dir or DOCS_SCREENSHOTS_DIR
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    transcription = parse_vtt(vtt_content)
    image_paths = extract_frames_from_video(video_path, out_dir, interval_sec, max_frames)
    documentation = generate_documentation(transcription, image_paths, openai_client)

    screenshots_base64 = get_screenshots_base64(image_paths) if image_paths else {}

    return {
        "documentation": documentation,
        "screenshots": [str(p) for p in image_paths],
        "screenshots_base64": screenshots_base64,
        "transcription": transcription,
    }
