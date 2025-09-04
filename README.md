# NeuroQuack

A flexible AI-powered API that acts as a hub between various input sources (Twitch, Discord, direct API) and AI services (Replicate, Bedrock, local models). Built with FastAPI and designed for easy deployment and scaling.

## Features

### Core API
- **Image Analysis**: CLIP interrogation and BLIP captioning
- **Image Generation**: SDXL text-to-image generation
- **Image Editing**: PhotoMaker for image transformation
- **Flexible Model Configuration**: Override models at API, environment, or app level

### Optional Integrations
- **Twitch Bot**: Chat commands for image processing
- **Discord Bot**: (Coming soon) Discord integration
- **Direct API**: RESTful endpoints for programmatic access

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- Replicate API token

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd NeuroQuack
   just run
   ```

2. **Configure API**:
   ```bash
   curl -X POST "http://localhost:8000/configure" \
        -H "Content-Type: application/json" \
        -d '{
          "api": {
            "replicate_token": "your_token_here",
            "replicate_org": "your_org_here"
          }
        }'
   ```

3. **Test image analysis**:
   ```bash
   curl -X POST "http://localhost:8000/image/analyze/clip" \
        -H "Content-Type: application/json" \
        -d '{
          "image_url": "https://example.com/image.jpg"
        }'
   ```

4. **Generate image**:
   ```bash
   curl -X POST "http://localhost:8000/image/generate" \
        -H "Content-Type: application/json" \
        -d '{
          "prompt": "a beautiful landscape"
        }'
   ```

### Docker Deployment

1. **Build and run**:
   ```bash
   just rebuild
   ```

2. **Configure with environment variables**:
   ```bash
   export REPLICATE_API_TOKEN="your_token"
   export REPLICATE_ORG="your_org"
   just docker-run
   ```

## API Endpoints

### Configuration
- `POST /configure` - Configure API tokens and optional bot integrations

### Image Processing
- `POST /image/analyze/clip` - Analyze image with CLIP interrogator
- `POST /image/analyze/blip` - Generate image caption with BLIP
- `POST /image/generate` - Generate image from text prompt
- `POST /image/photomaker` - Transform image using PhotoMaker

### Bot Control
- `POST /start_bot` - Start Twitch bot (if configured)
- `POST /stop_bot` - Stop Twitch bot

## Model Configuration

The system supports hierarchical model configuration:

1. **API Level** (highest priority): Specify model in API request
2. **Environment Level**: Set `MODEL_*` environment variables
3. **App Level** (lowest priority): Default models in `config/models.py`

### Environment Variables

```bash
# Required
REPLICATE_API_TOKEN=your_token
REPLICATE_ORG=your_org

# Optional model overrides
MODEL_PHOTOMAKER=jd7h/photomaker:latest
MODEL_CLIP_INTERROGATOR=pharmapsychotic/clip-interrogator:8151e1c9f47e696fa316146a2e35812ccf79cfc9eba05b11c7f450155102af70
MODEL_SDXL=stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc
MODEL_BLIP=ducktapedevops/blip
```

## Architecture

NeuroQuack follows a hub-and-spoke architecture pattern:

**Input Sources** flow into the **NeuroQuack API** which then routes to **AI Services**:

- **Input Sources**: Twitch Chat, Discord, Direct API calls
- **NeuroQuack API**: FastAPI application with Pydantic models, Docker containerization
- **AI Services**: Replicate models, AWS Bedrock, Local models

The API acts as a central hub that can accept requests from multiple sources and route them to appropriate AI services based on the request type and configuration.

**TODO**: Create a visual architecture diagram showing the hub-and-spoke pattern with input sources, the NeuroQuack API hub, and AI service destinations.

## Development

### Project Structure

The application is organized into the following directories:

- **app/config/** - Model configuration and settings
- **app/inputs/** - Bot integrations (Twitch, Discord)
- **app/models/** - Pydantic data models for API requests/responses
- **app/routers/** - FastAPI route handlers for different endpoints
- **app/tasks/** - AI service integrations and business logic
- **app/flavor/** - Style configurations and templates
- **app/main.py** - FastAPI application entry point

### Adding New Models

1. Add model to `config/models.py`
2. Create task function in `tasks/`
3. Add router endpoint in `routers/`
4. Update environment variables if needed

### Adding New Integrations

1. Create integration in `inputs/`
2. Add configuration model in `models/bot.py`
3. Update `/configure` endpoint in `main.py`

## Deployment

### ECS/Fargate
The application is designed to run on AWS ECS with:
- Environment variable configuration
- Health checks via `/configure` endpoint
- Optional Twitch/Discord bot integration

### Docker
```bash
docker build -t neuroquack .
docker run -e REPLICATE_API_TOKEN -e REPLICATE_ORG -p 8080:8080 neuroquack
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Your License Here]
```