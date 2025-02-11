import torch
import os
from tensorrt_llm.quantization import QuantConfig
from tensorrt_llm.logger import logger

def quantize_model(model_path, output_path, calibration_data_path=None):
    """Quantize model to INT8 using calibration data
    
    Args:
        model_path: Path to the original model
        output_path: Where to save the quantized model
        calibration_data_path: Path to calibration dataset
    """
    logger.info(f'Starting INT8 quantization for {model_path}')
    
    # Load calibration data if provided
    if calibration_data_path and os.path.exists(calibration_data_path):
        calib_data = torch.load(calibration_data_path)
    else:
        raise ValueError("Calibration data required for INT8 quantization")
    
    # Configure quantization
    quant_config = QuantConfig(
        algorithm='minmax',      # Quantization algorithm
        calibration_batches=100, # Number of batches for calibration
        cache_file='calibration.cache'
    )
    
    # Perform quantization
    with torch.no_grad():
        model = quant_config.quantize(model_path, calib_data)
        
    # Save quantized model
    torch.save(model.state_dict(), output_path)
    logger.info(f'Quantized model saved to {output_path}')
    
    return model

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', required=True, help='Path to the original model')
    parser.add_argument('--output-path', required=True, help='Where to save quantized model')
    parser.add_argument('--calibration-data', required=True, help='Path to calibration data')
    
    args = parser.parse_args()
    quantize_model(args.model_path, args.output_path, args.calibration_data)
