"""
Model Loader - Load base model and swap LoRA adapters
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from typing import List, Dict


class ModelLoader:
    """Load and manage base model with LoRA adapters"""
    
    def __init__(self, base_model_name: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"):
        self.base_model_name = base_model_name
        self.base_model = None  # The raw AutoModel
        self.model = None       # The PeftModel (base + adapters)
        self.tokenizer = None
        
    def load_base_model_once(self):
        """Load base model and tokenizer, only if not already loaded."""
        if self.base_model is not None:
            return # Already loaded
            
        print(f"Loading base model: {self.base_model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name, trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        print("✓ Base model loaded")
    
    def load_adapter(self, adapter_path: str, adapter_name: str):
        """
        Load a LoRA adapter onto the base model.
        Returns the single, shared PeftModel object.
        """
        self.load_base_model_once()
        print(f"Loading {adapter_name} adapter from {adapter_path}")
        
        if self.model is None:
            print("  This is the first adapter. Wrapping base model with PeftModel...")
            self.model = PeftModel.from_pretrained(
                self.base_model,
                adapter_path,
                adapter_name=adapter_name,
                torch_dtype=torch.float16
            )
        else:
            print(f"  PeftModel already exists. Adding {adapter_name} adapter...")
            self.model.load_adapter(
                adapter_path,
                adapter_name=adapter_name
            )
        
        print(f"  Setting {adapter_name} as active adapter.")
        self.model.set_adapter(adapter_name) 
        print(f"✓ {adapter_name} adapter loaded and set as active")
        
        return self.model
    
    def generate(self, model, prompt_str: str, max_length: int = 512, temperature: float = 0.3):
        """
        Generate text using a raw prompt string.
        """
        
        # --- START OF FIX ---
        # We no longer use chat templates. We use the raw prompt string directly.
        inputs = self.tokenizer(prompt_str, return_tensors="pt").to(model.device)
        # --- END OF FIX ---
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)
        return response
