import os
import argparse
from tensorrt_llm.builder import Builder
from tensorrt_llm.logger import logger

def optimize_model(model_path, output_path, precision='fp16', max_batch_size=1):
    """Optimize a model for TensorRT-LLM
    
    Args:
        model_path (str): Path to the input model
        output_path (str): Path to save the optimized model
        precision (str): Precision to use ('fp32', 'fp16', or 'int8')
        max_batch_size (int): Maximum batch size for inference
    """
    logger.info(f'Optimizing model from {model_path}')
    
    # Configure builder
    builder = Builder()
    builder.max_batch_size = max_batch_size
    builder.max_workspace_size = 8 * 1024 * 1024 * 1024  # 8GB
    
    # Set precision
    if precision == 'fp16':
        builder.fp16_mode = True
    elif precision == 'int8':
        builder.int8_mode = True
        
    # Build engine
    engine = builder.build_engine(model_path, output_path)
    
    logger.info(f'Optimized model saved to {output_path}')
    return engine

def main():
    parser = argparse.ArgumentParser(description='Optimize model for TensorRT-LLM')
    parser.add_argument('--model-path', required=True, help='Path to input model')
    parser.add_argument('--output-path', required=True, help='Path to save optimized model')
    parser.add_argument('--precision', choices=['fp32', 'fp16', 'int8'], default='fp16',
                        help='Precision for optimization')
    parser.add_argument('--batch-size', type=int, default=1, help='Maximum batch size')
    
    args = parser.parse_args()
    optimize_model(args.model_path, args.output_path, args.precision, args.batch_size)

if __name__ == '__main__':
    main()
