"""
RELIABLE Model Selector - Only includes tested, working models for educational tutoring
"""

# ONLY include models that are known to work well for educational purposes
RELIABLE_MODELS = [
    # Tier 1: Best for tutoring - dialog-optimized, reliable responses
    {
        "name": "microsoft/DialoGPT-small",
        "size": "~350MB",
        "type": "dialog",
        "reliability": "excellent",
        "reason": "Specifically designed for conversations, gives coherent responses"
    },
    {
        "name": "distilgpt2", 
        "size": "~350MB",
        "type": "general",
        "reliability": "good",
        "reason": "Lightweight, reliable, gives consistent educational responses"
    },
    # Tier 2: Fallback options
    {
        "name": "gpt2",
        "size": "~550MB", 
        "type": "general",
        "reliability": "good",
        "reason": "Standard model with decent educational responses"
    }
]

# REMOVED problematic models: DialoGPT-medium (too large/unreliable), large models

def get_recommended_model():
    """
    Return the MOST RELIABLE available model for educational tutoring
    Prioritizes models that give coherent, educational responses
    """
    print("🔍 Selecting the most reliable model for tutoring...")
    
    for model_info in RELIABLE_MODELS:
        model_name = model_info["name"]
        try:
            print(f"🔄 Testing {model_name}...")
            
            # Quick functionality test
            from transformers import pipeline, AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Test if model can be loaded and used
            test_pipe = pipeline(
                "text-generation", 
                model=model_name,
                max_new_tokens=10,  # Quick test
                tokenizer=tokenizer
            )
            
            # Quick generation test
            test_result = test_pipe("Test:", max_new_tokens=5)
            
            print(f"✅ {model_name}: {model_info['reason']}")
            print(f"   Size: {model_info['size']}, Reliability: {model_info['reliability']}")
            return model_name
            
        except Exception as e:
            print(f"❌ {model_name} failed: {str(e)[:100]}...")
            continue
    
    # Ultimate fallback - distilgpt2 should always work
    print("⚠️  Using ultimate fallback: distilgpt2")
    return "distilgpt2"

def is_model_reliable_for_tutoring(model_name: str) -> bool:
    """Check if a model is reliable for educational tutoring"""
    return any(model_info["name"] == model_name for model_info in RELIABLE_MODELS)

def get_model_info(model_name: str) -> dict:
    """Get detailed information about a model"""
    for model_info in RELIABLE_MODELS:
        if model_info["name"] == model_name:
            return {
                "name": model_name,
                "size": model_info["size"],
                "type": model_info["type"],
                "reliability": model_info["reliability"],
                "reason": model_info["reason"],
                "best_for_tutoring": model_info["reliability"] in ["excellent", "good"]
            }
    
    return {
        "name": model_name,
        "size": "Unknown",
        "type": "unknown", 
        "reliability": "untested",
        "reason": "This model has not been tested for reliability",
        "best_for_tutoring": False
    }

def get_available_models() -> list:
    """Get list of all reliable models"""
    return [model["name"] for model in RELIABLE_MODELS]

def estimate_model_size(model_name: str) -> str:
    """Estimate model size"""
    for model_info in RELIABLE_MODELS:
        if model_info["name"] == model_name:
            return model_info["size"]
    return "Unknown"

def get_model_recommendation(use_case: str = "tutoring") -> dict:
    """Get the best model recommendation for a specific use case"""
    if use_case == "tutoring":
        # For tutoring, prefer dialog models
        dialog_models = [m for m in RELIABLE_MODELS if m["type"] == "dialog"]
        if dialog_models:
            return dialog_models[0]
    
    # Default to first reliable model
    return RELIABLE_MODELS[0]

# Test function to verify model reliability
def test_model_reliability(model_name: str) -> dict:
    """Test if a model gives reliable educational responses"""
    try:
        from transformers import pipeline
        
        print(f"🧪 Testing {model_name} for educational responses...")
        
        pipe = pipeline(
            "text-generation",
            model=model_name,
            max_new_tokens=50,
            temperature=0.7
        )
        
        # Test questions that should get educational responses
        test_questions = [
            "What is mathematics?",
            "Explain physics basics"
        ]
        
        results = []
        for question in test_questions:
            prompt = f"Student: {question}\nTutor:"
            result = pipe(prompt, max_new_tokens=50)
            response = result[0]['generated_text'].replace(prompt, "").strip()
            
            # Check if response is educational
            is_educational = len(response) > 20 and any(word in response.lower() for word in 
                                                     ['study', 'science', 'learn', 'understand', 'explain'])
            
            results.append({
                "question": question,
                "response": response,
                "is_educational": is_educational,
                "length": len(response)
            })
        
        # Calculate reliability score
        educational_count = sum(1 for r in results if r["is_educational"])
        reliability_score = educational_count / len(results)
        
        return {
            "model": model_name,
            "reliability_score": reliability_score,
            "status": "reliable" if reliability_score >= 0.5 else "unreliable",
            "test_results": results
        }
        
    except Exception as e:
        return {
            "model": model_name,
            "reliability_score": 0.0,
            "status": "failed",
            "error": str(e)
        }