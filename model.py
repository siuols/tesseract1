from transformers import GPT2LMHeadModel, GPT2Tokenizer

def generate_text(input_text, model, tokenizer, max_length=1024):
    # Split input text into chunks
    chunk_size = max_length - len(tokenizer.eos_token)
    chunks = [input_text[i:i+chunk_size] for i in range(0, len(input_text), chunk_size)]

    generated_chunks = []
    for chunk in chunks:
        input_ids = tokenizer.encode(chunk, return_tensors='pt', max_length=max_length, truncation=True)
        # Ensure that the pad_token_id is set to the eos_token_id
        model.config.pad_token_id = model.config.eos_token_id
        # Generate text with sampling
        output = model.generate(input_ids, max_length=max_length, num_return_sequences=1, do_sample=True, temperature=0.7)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        generated_chunks.append(generated_text)
    
    return ' '.join(generated_chunks)

# Initialize model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def gpt_model(extracted_text: str) -> str:
    if extracted_text.strip() == "":
        print("Error: Extracted text is empty or contains only whitespace.")
    else:
        try:
            generated_text = generate_text(extracted_text, model, tokenizer)
            print(generated_text)
            return str(generated_text)
        except IndexError as e:
            print(f"Error: {e}")
            
        