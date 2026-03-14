import os
from huggingface_hub import InferenceClient

def generate_answer(query: str, context: list[str]) -> str:
    """
    Combines the user query with the retrieved context and asks an LLM for the answer.
    """
    if not context:
        context_text = "No relevant context found in the knowledge base."
    else:
        context_text = "\n".join([f"- {c}" for c in context])

    # HuggingFace Serverless Inference API is free and doesn't explicitly require a key for small use cases
    # although rate limits apply. If you have an HF key, put it in HF_TOKEN
    hf_token = os.environ.get("HF_TOKEN")
    
    try:
        # Initialize client (it will use the HF token if present in environment, else anonymous)
        client = InferenceClient(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            token=hf_token
        )

        prompt = f"""<s>[INST] You are DevAssist AI, a strictly precise developer assistant. 
Answer the user's question based ONLY on the provided context. If the context does not contain the answer or says no relevant context, strictly reply "I don't have enough information in my knowledge base to answer that."

Context:
{context_text}

User Question: {query} [/INST]"""

        # Generation
        response = client.text_generation(
            prompt,
            max_new_tokens=256,
            temperature=0.2,
            return_full_text=False
        )
        return response.strip()

    except Exception as e:
        # Fallback if rate limited or network error
        if not context:
            return "I couldn't find any information about that in my knowledge base. (Note: Set HF_TOKEN environment variable for better API limits.)"
        
        fallback = f"Based on the knowledge base: {context[0]}\n\n(AI generation failed: Rate limit or network error. Set HF_TOKEN environment variable.)"
        return fallback
