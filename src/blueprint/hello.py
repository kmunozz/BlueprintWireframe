import gradio as gr
import subprocess
import tempfile
import os

def get_ollama_response(image_path, user_prompt):
    """Run Ollama with embedded image + prompt and return raw XML code."""

    # Starting ollama incase it isnt
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # the system prompt so the model knows what to do
    system_prompt = (
        "You are a helpful assistant that converts UI wireframe sketches and descriptions into layout code.\n"
        "Given a sketch image and a prompt with more details about the sketch, output raw XML code representing the layout.\n"
        "Only output XML—no explanations, no formatting, no markdown.\n\n"
    )

    # the proper image syntax for ollama cli 
    image_embedding = f"<|im_start|>image\n{image_path}\n<|im_end|>\n"
    # Combine the full prompt
    full_prompt = image_embedding + system_prompt + user_prompt

    # Run ollama with the llava model, inputing the full prompt
    result = subprocess.run(
        ["ollama", "run", "llava"],
        input=full_prompt,
        text=True,
        capture_output=True
    )

    
    return result.stdout

# Creating a simple Gradio interface
iface = gr.Interface(
    fn=get_ollama_response,
    inputs=[
        gr.Image(type="filepath", label="Upload your wireframe sketch"),
        gr.Textbox(lines=4, placeholder="Describe the purpose or style of the website...", label="Prompt")
    ],
    outputs="text",
    title="Ollama Wireframe to XML Generator",
    description="Upload a wireframe sketch and describe the desired website to generate a skeleton in XML."
)

iface.launch()
