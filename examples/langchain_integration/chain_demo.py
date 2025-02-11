#!/usr/bin/env python3

from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
import torch

class LangChainDemo:
    def __init__(self):
        # Initialize language model
        pipe = pipeline(
            "text-generation",
            model="Llama-3.2-3B",
            torch_dtype=torch.float16,
            device=0
        )
        
        self.llm = HuggingFacePipeline(pipeline=pipe)
        
    def create_sensor_chain(self):
        """Create chain for sensor data analysis"""
        template = """
        Analyze these sensor readings:
        Temperature: {temperature}°C
        Humidity: {humidity}%
        Pressure: {pressure}hPa
        Gas: {gas}Ω
        
        Provide:
        1. Environmental conditions
        2. Health implications
        3. Recommended actions
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["temperature", "humidity", "pressure", "gas"]
        )
        
        return LLMChain(llm=self.llm, prompt=prompt)
    
    def create_vision_chain(self):
        """Create chain for vision analysis"""
        template = """
        Analyze this image content:
        {image_description}
        
        Identify:
        1. Key objects
        2. Activities
        3. Safety concerns
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["image_description"]
        )
        
        return LLMChain(llm=self.llm, prompt=prompt)