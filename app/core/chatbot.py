"""
Chatbot Tutor - USING RELIABLE MODELS ONLY
"""
import re
from typing import List, Dict, Any

from .memory import ChatMemory
from .rag import RAGSystem
from .model_selector import get_recommended_model, is_model_reliable_for_tutoring

class TutorChatbot:
    def __init__(self, model_name: str = None, use_rag: bool = True):
        """
        Initialize chatbot with RELIABLE model selection
        """
        # Use recommended RELIABLE model if none specified
        if model_name is None:
            model_name = get_recommended_model()
        
        # Validate model reliability
        if not is_model_reliable_for_tutoring(model_name):
            print(f"⚠️  Warning: {model_name} is not in the reliable models list")
            # Fall back to recommended model
            model_name = get_recommended_model()
        
        self.model_name = model_name
        self.use_rag = use_rag
        self.memory = ChatMemory()
        self.rag_system = RAGSystem() if use_rag else None
        
        print(f"🎯 Using reliable model: {model_name}")
        
        # Initialize the model pipeline
        self.pipe = self._initialize_model_pipeline(model_name)
        
        print(f"✅ Chatbot ready with reliable model")
        print(f"✅ RAG: {use_rag}")

    def _initialize_model_pipeline(self, model_name: str):
        """Initialize model pipeline with RELIABLE settings"""
        try:
            from transformers import pipeline, AutoTokenizer
            
            print(f"🔄 Loading {model_name}...")
            
            # Get tokenizer first
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Add padding token if needed
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            # RELIABLE settings for educational responses
            pipe = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=tokenizer,
                max_new_tokens=100,  # Conservative length
                temperature=0.7,     # Balanced creativity
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                return_full_text=False  # Don't include prompt
            )
            
            print("✅ Model pipeline created successfully")
            return pipe
            
        except Exception as e:
            print(f"❌ Model initialization failed: {e}")
            return None

    def generate_response(self, user_input: str) -> str:
        """Generate response using RELIABLE approach"""
        self.memory.add_message(user_input, is_user=True)
        
        # Try model generation first (if available and reliable)
        if self.pipe is not None:
            model_response = self._generate_with_reliable_model(user_input)
            
            # Use model response if it's good quality
            if self._is_quality_response(model_response, user_input):
                self.memory.add_message(model_response, is_user=False)
                return model_response
        
        # Fall back to high-quality rule-based responses
        rule_response = self._generate_high_quality_rule_based(user_input)
        self.memory.add_message(rule_response, is_user=False)
        return rule_response

    def _generate_with_reliable_model(self, user_input: str) -> str:
        """Generate response using reliable model with EDUCATIONAL prompts"""
        try:
            # Get context from RAG if enabled
            context = ""
            if self.use_rag and self.rag_system:
                relevant_docs = self.rag_system.retrieve_relevant_documents(user_input, n_results=1)
                if relevant_docs:
                    context = f"Reference: {relevant_docs[0]['document'][:200]}\n\n"
            
            # RELIABLE educational prompt
            prompt = self._create_educational_prompt(user_input, context)
            
            print(f"📝 Using educational prompt for: {user_input}")
            
            # Generate with reliable settings
            result = self.pipe(
                prompt,
                max_new_tokens=80,  # Conservative length
                temperature=0.7,    # Balanced
                do_sample=True
            )
            
            # Extract and clean response
            response = result[0]['generated_text'].strip()
            response = self._clean_model_response(response, prompt)
            
            print(f"🤖 Model generated: {response[:80]}...")
            return response
            
        except Exception as e:
            print(f"❌ Model generation error: {e}")
            return ""

    def _create_educational_prompt(self, user_input: str, context: str = "") -> str:
        """Create RELIABLE educational prompt"""
        # Simple, effective prompt structure
        prompt_parts = []
        
        # System message
        prompt_parts.append("You are a knowledgeable tutor. Provide clear, accurate explanations.")
        
        # Add context if available
        if context:
            prompt_parts.append(f"Background information:\n{context}")
        
        # Current question
        prompt_parts.append(f"Student question: {user_input}")
        prompt_parts.append("Tutor explanation:")
        
        return "\n\n".join(prompt_parts)

    def _clean_model_response(self, response: str, prompt: str) -> str:
        """Clean model response reliably"""
        if not response:
            return ""
        
        # Remove prompt if included
        response = response.replace(prompt, "").strip()
        
        # Remove common garbage patterns
        garbage_patterns = [
            r"English please\??",
            r"please explain.*",
            r"I don't understand.*",
            r"can you repeat.*",
            r"what do you mean.*",
            r"\?+$"  # Multiple question marks
        ]
        
        for pattern in garbage_patterns:
            response = re.sub(pattern, "", response, flags=re.IGNORECASE)
        
        # Clean whitespace
        response = ' '.join(response.split())
        
        return response

    def _is_quality_response(self, response: str, user_input: str) -> bool:
        """Check if response is quality educational content"""
        if not response or len(response.strip()) < 15:
            return False
        
        # Reject obvious bad responses
        bad_indicators = [
            "english please", "please explain", "i don't understand",
            "can you repeat", "what do you mean", "??", "..."
        ]
        
        if any(indicator in response.lower() for indicator in bad_indicators):
            return False
        
        # Response should be substantially different from input
        if response.lower() == user_input.lower():
            return False
        
        # Should contain educational content
        educational_indicators = [
            'is', 'are', 'study', 'science', 'learn', 'understand', 
            'explain', 'example', 'called', 'means', 'includes'
        ]
        
        has_educational_content = any(indicator in response.lower() for indicator in educational_indicators)
        
        return has_educational_content

    def _generate_high_quality_rule_based(self, user_input: str) -> str:
        """High-quality educational responses as fallback"""
        user_input_lower = user_input.lower()
        
        # EXTENSIVE knowledge base with detailed explanations
        knowledge_base = {
            "math": """Mathematics is the study of numbers, quantities, shapes, patterns, and relationships. It's divided into several main areas:

• Arithmetic: Basic operations with numbers
• Algebra: Solving equations using variables
• Geometry: Studying shapes, sizes, and spatial relationships  
• Calculus: Analyzing change and motion
• Statistics: Collecting, analyzing, and interpreting data

Mathematics develops logical thinking and problem-solving skills that are valuable in many fields.""",

            "mathematics": """Mathematics is a fundamental discipline that explores abstract structures and patterns. Key branches include:

- Pure Mathematics: Number theory, algebra, geometry
- Applied Mathematics: Calculus, statistics, optimization
- Discrete Mathematics: Logic, graph theory, combinatorics

Mathematics provides the language and tools for science, engineering, economics, and technology.""",

            "physics": """Physics is the natural science that studies matter, energy, and the fundamental forces of nature. Major areas include:

• Classical Mechanics: Motion of objects (Newton's laws)
• Thermodynamics: Heat, temperature, and energy transfer  
• Electromagnetism: Electricity, magnetism, and light
• Quantum Mechanics: Behavior of atoms and particles
• Relativity: High-speed and gravitational physics

Physics helps us understand how the universe works at every scale.""",

            "programming": """Programming involves writing instructions for computers to execute. Key concepts:

• Variables: Store and manage data
• Functions: Reusable blocks of code
• Control Structures: Loops and conditionals
• Algorithms: Step-by-step problem-solving procedures

Popular programming languages include Python, Java, JavaScript, and C++. Programming enables software development, data analysis, and automation.""",

            "calculus": """Calculus is the mathematics of continuous change. It has two main branches:

Differential Calculus: Studies rates of change (derivatives)
- Used for optimization, motion analysis, and growth rates

Integral Calculus: Studies accumulation (integrals)  
- Used for area calculation, volume, and total change

Calculus is essential for physics, engineering, economics, and computer science.""",

            "algebra": """Algebra uses symbols and variables to represent numbers and relationships. Key concepts:

• Variables: Symbols that represent unknown values
• Equations: Mathematical statements of equality
• Functions: Relationships between variables
• Polynomials: Expressions with variables and coefficients

Algebra provides the foundation for advanced mathematics and problem-solving.""",

            "java": """Java is a popular, object-oriented programming language known for:

• Platform Independence: "Write once, run anywhere" using the JVM
• Object-Oriented: Organizes code into classes and objects
• Strong Typing: Variables have specific data types
• Automatic Memory Management: Garbage collection handles memory

Java is widely used for enterprise applications, Android development, and large-scale systems.""",

            "python": """Python is a high-level programming language valued for:

• Readability: Clean, English-like syntax
• Versatility: Used for web development, data science, AI, and automation
• Large Ecosystem: Extensive libraries and frameworks
• Beginner-Friendly: Easy to learn and use

Python is popular in scientific computing, machine learning, and rapid prototyping."""
        }
        
        # Enhanced keyword matching
        keyword_mapping = {
            "math": ["math", "calculate", "equation", "number", "arithmetic"],
            "mathematics": ["mathematics", "maths", "mathematical"],
            "physics": ["physics", "motion", "force", "energy", "newton", "einstein"],
            "programming": ["programming", "code", "computer", "software", "developer"],
            "calculus": ["calculus", "derivative", "integral", "differentiation"],
            "algebra": ["algebra", "equation", "variable", "polynomial"],
            "java": ["java", "jvm", "object-oriented"],
            "python": ["python", "pandas", "numpy", "django"]
        }
        
        # Exact topic matches
        for topic, answer in knowledge_base.items():
            if topic in user_input_lower:
                return answer
        
        # Keyword matches
        for topic, keywords in keyword_mapping.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return knowledge_base[topic]
        
        # Greeting responses
        if any(word in user_input_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm your AI tutor. I can help you learn about mathematics, physics, programming, calculus, algebra, and other STEM subjects. What specific topic would you like to explore?"
        
        # Help response
        if "help" in user_input_lower:
            return """I can help you learn about these topics:

• Mathematics: Algebra, calculus, geometry
• Physics: Mechanics, thermodynamics, electromagnetism  
• Programming: Python, Java, algorithms
• Computer Science: Data structures, algorithms

What specific subject interests you?"""
        
        # Default educational response
        return "I'd be happy to help you learn! Please ask me about specific topics like mathematics, physics, programming, calculus, algebra, or computer science concepts. What would you like to know more about?"

    def clear_conversation(self):
        """Clear conversation memory"""
        self.memory.clear_memory()
        print("✅ Conversation memory cleared")