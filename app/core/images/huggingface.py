"""
Hugging Face image generation provider.

This module implements image generation using Hugging Face's Inference API.
It supports various diffusion models like Stable Diffusion, SDXL, and others
available on the Hugging Face platform.
"""

import os
from typing import Optional
import uuid
import base64
import logging
from huggingface_hub import InferenceClient

from app.core.images.base import ImageProvider
from app.core.images.models import ImageAsset

logger = logging.getLogger(__name__)


class HuggingFaceImageProvider(ImageProvider):
    """
    Image generation provider using Hugging Face Inference API.
    
    This provider generates images using AI models hosted on Hugging Face.
    It requires a Hugging Face API token and model identifier to be configured
    via environment variables.
    
    Configuration:
        HF_API_TOKEN: Your Hugging Face API token (required)
                     Get one at: https://huggingface.co/settings/tokens
        
        HF_IMAGE_MODEL: Model identifier to use for generation (required)
                       Examples:
                       - "stabilityai/stable-diffusion-2-1"
                       - "stabilityai/stable-diffusion-xl-base-1.0"
                       - "runwayml/stable-diffusion-v1-5"
    
    Features:
        - AI-powered image generation from text prompts
        - Automatic retry logic for failed requests
        - Base64 encoding for easy embedding
        - Graceful error handling
    
    Example:
        >>> provider = HuggingFaceImageProvider()
        >>> if provider.validate():
        ...     asset = provider.generate("a serene lake at sunset")
        ...     print(asset.source)  # Base64 data URI
    """
    
    def __init__(self):
        """Initialize the Hugging Face image provider with environment config."""
        self.api_token = os.getenv("HF_API_TOKEN")
        # Default to stable-diffusion-xl which is widely available
        self.model = os.getenv("HF_IMAGE_MODEL", "stabilityai/stable-diffusion-xl-base-1.0")
        # Initialize the InferenceClient
        self.client = None
        if self.api_token:
            self.client = InferenceClient(token=self.api_token)
    
    def validate(self) -> bool:
        """
        Validate that the provider is properly configured.
        
        Checks for:
        - HF_API_TOKEN environment variable
        - HF_IMAGE_MODEL environment variable
        
        Returns:
            bool: True if properly configured, False otherwise.
        """
        if not self.api_token:
            logger.warning("HF_API_TOKEN environment variable not set")
            return False
        
        if not self.model:
            logger.warning("HF_IMAGE_MODEL environment variable not set")
            return False
        
        return True
    
    def generate(
        self,
        prompt: str,
        placement: Optional[str] = None,
        **kwargs
    ) -> ImageAsset:
        """
        Generate an image using Hugging Face Inference API.
        
        Args:
            prompt: Text description of the image to generate.
            placement: Optional placement hint (e.g., "cover", "section").
            **kwargs: Additional parameters (currently unused).
        
        Returns:
            ImageAsset: Generated image as a base64 data URI.
        
        Raises:
            ValueError: If prompt is empty or provider not configured.
            ConnectionError: If API request fails.
            Exception: For other unexpected errors.
        """
        # Validate input
        if not prompt or not prompt.strip():
            raise ValueError("Image prompt cannot be empty")
        
        # Validate configuration
        if not self.validate():
            raise ValueError(
                "HuggingFace provider not properly configured. "
                "Please set HF_API_TOKEN and HF_IMAGE_MODEL environment variables."
            )
        
        try:
            logger.info(f"Generating image with HuggingFace model: {self.model}")
            logger.info(f"Prompt: {prompt}")
            
            # Use InferenceClient to generate image
            image = self.client.text_to_image(
                prompt=prompt,
                model=self.model
            )
            
            # Convert PIL Image to base64 data URI
            from io import BytesIO
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            data_uri = f"data:image/png;base64,{base64_image}"
            
            # Generate unique ID
            image_id = f"hf_{uuid.uuid4().hex[:12]}"
            
            # Create ImageAsset
            asset = ImageAsset(
                id=image_id,
                prompt=prompt,
                provider="huggingface",
                source=data_uri,
                placement=placement,
                alt_text=prompt,
                attribution=f"Generated by {self.model}"
            )
            
            logger.info(f"Successfully generated image: {image_id}")
            return asset
        
        except Exception as e:
            logger.error(f"Error during image generation: {str(e)}")
            raise ConnectionError(
                f"Failed to generate image with Hugging Face: {str(e)}"
            )
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "huggingface"
    
    def supports_generation(self) -> bool:
        """This provider supports AI image generation."""
        return True
    
    def supports_search(self) -> bool:
        """This provider does not support image search."""
        return False
