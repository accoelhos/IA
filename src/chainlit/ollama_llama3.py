import chainlit as cl
import requests

# Define the API endpoint for Ollama
OLLAMA_API_URL = "http://austrinus.eic.cefet-rj.br:11434/api/generate"

@cl.on_message
async def on_message(message: cl.Message):
    """Handle user messages and send responses from Llama 3.1."""
    
    # Prepare the payload
    payload = {
        "model": "llama3.1",
        "prompt": message.content
    }
    
    # Send request to Ollama
    response = requests.post(OLLAMA_API_URL, json=payload)
    
    if response.status_code == 200:
        generated_text = response.json().get("text", "Error: No response from Llama 3.1")
    else:
        generated_text = f"Error {response.status_code}: {response.text}"
    
    # Send response back to the Chainlit UI
    await message.reply(generated_text)

# Run the Chainlit app
if __name__ == "__main__":
    cl.run()
