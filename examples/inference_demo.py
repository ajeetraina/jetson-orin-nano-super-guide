import torch
from tensorrt_llm.runtime import ModelConfig, SamplingConfig
from tensorrt_llm.runtime import GenerationSession, Model

class InferenceDemo:
    def __init__(self, model_path):
        """Initialize the inference demo with a TensorRT-LLM optimized model"""
        self.config = ModelConfig(
            max_batch_size=1,
            max_input_len=512,
            max_output_len=128
        )
        self.model = Model(model_path, self.config)
        self.session = GenerationSession(self.model)
        
    def generate_response(self, prompt, max_length=128):
        """Generate a response for the given prompt"""
        sampling_config = SamplingConfig(
            max_new_tokens=max_length,
            temperature=0.7
        )
        
        outputs = self.session.generate(
            [prompt],
            sampling_config
        )
        
        return outputs[0]

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run inference with TensorRT-LLM model')
    parser.add_argument('--model-path', required=True, help='Path to the optimized model')
    parser.add_argument('--input', required=True, help='Input prompt')
    parser.add_argument('--max-length', type=int, default=128, help='Maximum response length')
    
    args = parser.parse_args()
    
    # Initialize demo
    demo = InferenceDemo(args.model_path)
    
    # Generate response
    response = demo.generate_response(args.input, args.max_length)
    print(f"\nResponse: {response}")

if __name__ == '__main__':
    main()