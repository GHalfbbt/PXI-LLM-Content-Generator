"""
Replicate AI image generation provider.

This module implements AI-powered image generation using Replicate's API.
It uses Stable Diffusion XL (SDXL) or other models to generate images from
text prompts.
"""

import os
import logging
from typing import Optional
import replicate

from app.core.images.base import ImageProvider
from app.core.images.models import ImageAsset

logger = logging.getLogger(__name__)


class ReplicateImageProvider(ImageProvider):
    """
    Image provider for Replicate AI image generation.
    
    This provider generates images using AI models hosted on Replicate,
    such as Stable Diffusion XL (SDXL). It creates new images based on
    text prompts rather than searching for existing images.
    
    Configuration:
        REPLICATE_API_TOKEN: API token for Replicate (required)
                            Get one at: https://replicate.com/account/api-tokens
        
        REPLICATE_IMAGE_MODEL: Model to use for generation (optional)
                              Default: "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
                              
                              Popular models:
                              - stability-ai/sdxl (Stable Diffusion XL)
                              - stability-ai/stable-diffusion (SD 2.1)
    
    Features:
        - AI-powered image generation
        - High-quality, customizable outputs
        - Multiple model support
        - Text-to-image generation
    
    Example:
        >>> provider = ReplicateImageProvider()
        >>> if provider.validate():
        ...     asset = provider.generate("mountain landscape at sunset")
        ...     print(asset.source)  # HTTPS URL to generated image
    """
    
    # Default model: Stable Diffusion XL
    DEFAULT_MODEL = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
    
    def __init__(self):
        """Initialize the Replicate image provider with environment config."""
        self.api_token = os.getenv("REPLICATE_API_TOKEN")
        self.model = os.getenv("REPLICATE_IMAGE_MODEL", self.DEFAULT_MODEL)
        
        # Configure Replicate client if token is available
        if self.api_token:
            os.environ["REPLICATE_API_TOKEN"] = self.api_token
    
    def validate(self) -> bool:
        """
        Validate that Replicate is properly configured.
        
        Returns:
            bool: True if API token is set, False otherwise.
        """
        if not self.api_token:
            logger.warning("Replicate API token not configured")
            logger.info("Set REPLICATE_API_TOKEN to enable AI image generation")
            return False
        
        return True
    
    def generate(
        self,
        prompt: str,
        placement: Optional[str] = None,
        **kwargs
    ) -> ImageAsset:
        """
        Generate an image using Replicate AI.
        
        Args:
            prompt: Text description of the image to generate.
            placement: Optional placement hint (may affect generation params).
            **kwargs: Additional parameters:
                     - width: Image width in pixels (default: 1024)
                     - height: Image height in pixels (default: 1024)
                     - num_inference_steps: Number of denoising steps (default: 50)
                     - guidance_scale: How closely to follow prompt (default: 7.5)
                     - negative_prompt: What to avoid in the image
        
        Returns:
            ImageAsset: Generated image with URL.
        
        Raises:
            ValueError: If prompt is empty or configuration invalid.
            ConnectionError: If Replicate API request fails.
        """
        # Validate input
        if not prompt or not prompt.strip():
            raise ValueError("Image generation prompt cannot be empty")
        
        # Validate configuration
        if not self.validate():
            raise ValueError(
                "Replicate provider not configured. "
                "Please set REPLICATE_API_TOKEN environment variable."
            )
        
        try:
            # Prepare input parameters
            input_params = {
                "prompt": prompt,
                "width": kwargs.get("width", 1024),
                "height": kwargs.get("height", 1024),
                "num_inference_steps": kwargs.get("num_inference_steps", 50),
                "guidance_scale": kwargs.get("guidance_scale", 7.5),
            }
            
            # Add negative prompt if provided
            if "negative_prompt" in kwargs:
                input_params["negative_prompt"] = kwargs["negative_prompt"]
            
            logger.info(f"Generating image with Replicate: prompt='{prompt}', model='{self.model}'")
            
            # Run the model
            output = replicate.run(
                self.model,
                input=input_params
            )
            
            # Output can be a list or a single URL
            if isinstance(output, list):
                image_url = output[0] if output else None
            else:
                image_url = output
            
            if not image_url:
                raise ConnectionError("Replicate API returned empty response")
            
            # Create ImageAsset
            asset = ImageAsset(
                id=f"replicate_{hash(prompt)}",
                prompt=prompt,
                provider="replicate",
                source=str(image_url),
                placement=placement,
                alt_text=f"AI-generated image: {prompt}",
                attribution="Generated by Replicate AI (Stable Diffusion XL)"
            )
            
            logger.info(f"Successfully generated image: {asset.id}")
            return asset
            
        except replicate.exceptions.ReplicateError as e:
            logger.error(f"Replicate API error: {str(e)}")
            raise ConnectionError(f"Failed to generate image with Replicate: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during Replicate generation: {str(e)}")
            raise ConnectionError(f"Image generation failed: {str(e)}")
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "replicate"
    
    def supports_generation(self) -> bool:
        """This provider supports AI image generation."""
        return True
    
    def supports_search(self) -> bool:
        """This provider does not support image search."""
        return False
