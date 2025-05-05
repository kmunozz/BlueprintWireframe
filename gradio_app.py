import gradio as gr
from ai_models import get_llama3_wireframe
import base64
import zlib

def generate_preview_link(xml_str):
    # Create a raw DEFLATE compressor (wbits=-15 removes headers)
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed = compressor.compress(xml_str.encode("utf-8")) + compressor.flush()

    base64_xml = base64.b64encode(compressed).decode("utf-8")

    # Embed-friendly URL with no URI encoding!
    return f"https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1#R{base64_xml}"


def generate_wireframe(prompt):
    if not prompt.strip():
        return "", None, "", prompt

    wireframe_xml = get_llama3_wireframe(prompt)

    file_path = "latest.xml"
    with open(file_path, "w") as f:
        f.write(wireframe_xml)

    preview_url = generate_preview_link(wireframe_xml)
    preview_md = f"[🔗 Click to Preview in Draw.io]({preview_url})"

    return wireframe_xml, file_path, preview_md, prompt

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Mozilla Wireframe Generator\nGenerate editable draw.io wireframes using a simple text prompt.")

    prompt_box = gr.Textbox(label="Prompt", placeholder="e.g., A homepage for a fitness app")

    with gr.Row():
        generate_btn = gr.Button("Generate Wireframe")
        regenerate_btn = gr.Button("Regenerate", variant="secondary")

    xml_output = gr.Textbox(label="Generated Wireframe XML")
    download_output = gr.File(label="📥 Click to Download Latest Wireframe XML")
    preview_link = gr.Markdown()

    generate_btn.click(
        fn=generate_wireframe,
        inputs=[prompt_box],
        outputs=[xml_output, download_output, preview_link, prompt_box]
    )

    regenerate_btn.click(
        fn=generate_wireframe,
        inputs=[prompt_box],
        outputs=[xml_output, download_output, preview_link, prompt_box]
    )

print(" Starting Gradio app...")
demo.launch()
