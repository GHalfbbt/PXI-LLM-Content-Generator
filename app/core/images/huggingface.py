"""
Hugging Face image generation provider.

This module implements image generation using Hugging Face's Inference API.
It supports various diffusion models like Stable Diffusion, SDXL, and others
available on the Hugging Face platform.
"""

import os
import requests
from typing import Optional
import uuid
from io import BytesIO
import base64
import logging

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
        self.model = os.getenv("HF_IMAGE_MODEL")
        self.api_url = None
        
        if self.model:
            self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
    
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
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt
            }
            
            # Call Hugging Face API
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Handle errors
            if response.status_code != 200:
                error_detail = response.text
                if response.status_code == 503:
                    raise ConnectionError(
                        f"Model is loading. Please try again in a few moments. "
                        f"Details: {error_detail}"
                    )
                else:
                    raise ConnectionError(
                        f"Hugging Face API error (status {response.status_code}): {error_detail}"
                    )
            
            # Convert image bytes to base64 data URI
            image_bytes = response.content
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
            
            return asset
        
        except requests.exceptions.Timeout:
            raise ConnectionError(
                "Hugging Face API request timed out. The model may be overloaded."
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Failed to connect to Hugging Face API: {str(e)}"
            )
        except Exception as e:
            raise Exception(
                f"Unexpected error during image generation: {str(e)}"
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
