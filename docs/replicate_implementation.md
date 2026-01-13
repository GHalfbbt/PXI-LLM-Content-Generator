# Replicate AI Image Provider Implementation

## Overview
Successfully implemented Replicate AI as a third image generation provider for the content generation platform. Replicate offers stable, production-ready AI image generation using Stable Diffusion XL and other models.

## Files Created/Modified

### New Files
1. **app/core/images/replicate.py** - Replicate provider implementation
   - Class: `ReplicateImageProvider`
   - Uses official `replicate` Python SDK
   - Default model: Stable Diffusion XL (SDXL)
   - Supports customizable generation parameters

2. **app/scripts/test_replicate.py** - Test script for Replicate provider
   - Validates configuration
   - Tests image generation
   - Provides detailed output

### Modified Files
1. **app/core/images/factory.py**
   - Added import for `ReplicateImageProvider`
   - Registered "replicate" in `_PROVIDERS` registry
   - Updated docstrings to mention Replicate

2. **requirements.txt**
   - Added `replicate>=0.25.0` dependency

3. **.env.example**
   - Added Replicate configuration section
   - Environment variables:
     - `REPLICATE_API_TOKEN` (required)
     - `REPLICATE_IMAGE_MODEL` (optional, defaults to SDXL)

## Implementation Details

### ReplicateImageProvider Class

#### Configuration
```python
REPLICATE_API_TOKEN=<your_token_here>
REPLICATE_IMAGE_MODEL=stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b
```

#### Key Methods
- `validate()` - Checks if API token is configured
- `generate(prompt, placement, **kwargs)` - Generates images via Replicate API
- `provider_name` property - Returns "replicate"
- `supports_generation()` - Returns True (AI generation)
- `supports_search()` - Returns False (not a search provider)

#### Generation Parameters
The provider accepts these kwargs:
- `width` - Image width in pixels (default: 1024)
- `height` - Image height in pixels (default: 1024)
- `num_inference_steps` - Denoising steps (default: 50)
- `guidance_scale` - Prompt adherence strength (default: 7.5)
- `negative_prompt` - What to avoid in the image

#### Error Handling
- Raises `ValueError` for invalid configuration or empty prompts
- Raises `ConnectionError` for API failures
- Logs all operations and errors
- Gracefully handles edge cases

### Factory Registration
The Replicate provider is now available through the factory:

```python
from app.core.images.factory import ImageProviderFactory

# Get supported providers
providers = ImageProviderFactory.get_supported_providers()
# Returns: ['huggingface', 'external', 'replicate']

# Create Replicate provider
provider = ImageProviderFactory.create_provider("replicate")

# Generate image
asset = provider.generate("mountain landscape at sunset")
```

## Integration Status

### ✅ Already Integrated
The UI was already prepared for Replicate in the previous implementation:
- Sidebar controls include "replicate" option in radio buttons
- Blog image generation supports "replicate" provider
- Social post image generation supports "replicate" provider
- Error handling is in place for provider failures

### Testing
Verified functionality:
- ✅ Module imports successfully
- ✅ Factory registration working
- ✅ Provider instantiation working
- ✅ Capabilities correctly identified (generation: True, search: False)

## Usage in Application

### For Blog Content
Users can now select "Replicate AI (Stable Diffusion)" in the sidebar:
1. Check "Enable images for blog content"
2. Select "Replicate AI (Stable Diffusion)" as provider
3. Choose number of images (1-5)
4. Generate content - images will be AI-generated and embedded

### For Social Posts
Users can select Replicate for social media images:
1. Check "Include image in social posts"
2. Select "Replicate AI (Stable Diffusion)" as provider
3. Generate post - AI-generated image will be included in metadata

## Provider Comparison

| Feature | External (Unsplash/Pexels) | HuggingFace | Replicate |
|---------|---------------------------|-------------|-----------|
| Type | Stock photos | AI Generation | AI Generation |
| Status | ✅ Working | ⚠️ Deprecated API | ✅ Working |
| Quality | High (real photos) | Varies | High (SDXL) |
| Cost | Free (rate limited) | Free (limited) | Pay per use |
| Speed | Fast (1-2s) | N/A | Medium (10-30s) |
| Customization | Search-based | High | High |
| Attribution | Required | Not required | Not required |

## Next Steps

### To Use Replicate
1. Get API token from https://replicate.com/account/api-tokens
2. Add to `.env` file:
   ```
   REPLICATE_API_TOKEN=your_token_here
   ```
3. (Optional) Customize model:
   ```
   REPLICATE_IMAGE_MODEL=stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b
   ```
4. Select "Replicate AI" in the UI sidebar
5. Generate content with AI images

### Testing
Run the test script to verify setup:
```bash
python app/scripts/test_replicate.py
```

### Optional Enhancements (Future)
- Add more Replicate models (SD 1.5, SD 2.1, etc.)
- Implement advanced generation parameters in UI
- Add image size presets for different content types
- Cache generated images to avoid regeneration costs

## Technical Notes

### Model Selection
The default model is SDXL with a specific version hash. This ensures:
- Consistent, reproducible results
- High-quality outputs
- Stable API compatibility

To use a different model, update `REPLICATE_IMAGE_MODEL` in `.env`.

### API Response Handling
Replicate's API returns either:
- A single URL (string)
- A list of URLs (for multi-image generation)

The provider handles both cases and extracts the first image URL.

### Cost Considerations
Replicate charges per generation:
- SDXL: ~$0.03-0.05 per image
- Generation time: 10-30 seconds
- No free tier for generation

For cost-effective testing, use External provider (Unsplash/Pexels) which is free.

## Summary
The Replicate provider is now fully implemented and integrated into the content generation platform. It provides a production-ready alternative to HuggingFace (which has a deprecated API) and complements the External provider (stock photos) with true AI image generation capabilities.
