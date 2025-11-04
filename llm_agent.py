from google import genai
from google.genai import types
from transformers import  AutoModelForCausalLM, AutoTokenizer
from transformers import GPT2Tokenizer, GPT2Model
import torch 
import os

def setup_gemini(api_key):
    client =genai.Client(api_key=api_key)
    return client
def gemini_move(board,symbol,client):
    prompt = f"""
    You are playing Tic-Tac-Toe as '{symbol}'.
    Current board (index 0-8):
    {board}
    after your opponent's turn
    Respond with ONLY the index (0-8) where you want to play.
    """
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        config = types.GenerateContentConfig(
            system_instruction = "You are a very competitive and strategic Tic-Tac-Toe player"
        ),
        contents = prompt

    )

    return int(response.text)


def load_local_model(model_name="mistralai/Mistral-7B-Instruct-v0.2"):
    # Determine the device
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")

    # Set the appropriate torch_dtype for the device
    dtype = torch.float16 if device == "mps" else torch.float32

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # 1. Load model without 'device_map'
    #    The model is loaded to CPU first by default
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=dtype,  # Use the determined dtype
        # REMOVE: device_map={"": device}  <-- This line caused the error!
    )
    
    # 2. Explicitly move the model to the target device (MPS or CPU)
    model.to(device)

    model.eval()
    return model, tokenizer, device


# Generate a move with GPT-2
def local_llm_move(board, symbol, model, tokenizer, device):
    """
    board: list of 9 positions [' ', 'X', 'O', ...]
    symbol: 'X' or 'O'
    """
    # Use a simpler, continuous pattern
    few_shot = """
Board: ['X', ' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ']
AI ('X'): 1

Board: ['X', 'O', 'X', ' ', 'O', ' ', ' ', ' ', ' ']
AI ('O'): 3

Board: ['O', 'X', ' ', 'X', 'O', ' ', ' ', ' ', ' ']
AI ('O'): 5

# Start your turn immediately, continuing the pattern
"""

    # CRITICAL: Append the board and the AI prompt exactly matching the examples
    prompt = prompt = f"""
    You are a professional Tic-Tac-Toe AI playing as '{symbol}'.
    The current board state is represented as a list of 9 indices (0-8): {board}
    
    RULES: You must respond with ONLY a single digit (0-8) that corresponds to an empty position (' ') on the board.
    
    Move:""" # Removed the space after the colon
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Use max_new_tokens=2 to force the model to generate only the number
    # Also, slightly reduce the temperature to make the output less creative (i.e., less text)
    output = model.generate(
        **inputs,
        max_new_tokens=2, # <--- Even more aggressive token limit
        temperature=0.1,  # <--- Lowered temperature for less "rambling"
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    # Extract newly generated tokens
    generated_tokens = output[0][inputs['input_ids'].shape[-1]:]
    response = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
    
    print("Raw Model Response:", response)
    
    # Extract the first valid digit (0-8)
    for char in response:
        if char.isdigit():
            move = int(char)
            if 0 <= move <= 8 and board[move] == ' ':
                print(f"GPT-2 move: {move}")
                return move

    # fallback if nothing valid
    return -1



