# NeuroQuack

NeuroQuack is an innovative platform combining the power of conversational AI and advanced image synthesis to create a unique interactive experience. It allows users to upload images and engage with an AI to transform those images into personalized caricatures. Dive into a generative world where every conversation with the AI leads to a new visual discovery.

![Alt Text](./media/images/real-mvp.gif)

MVP: Minimal Viable Product
- Docker Container running locally for Twitch Bot with interaction with chat
- Deployable to AWS
- Walkthrough

FMVP: Finals MVP
- Integration with a Large Language Model (LLM) for dynamic conversation flow.
- Utilization of Stable Diffusion for real-time image generation based on LLM prompts.
- AWS SageMaker for hosting and auto-scaling the LLM and Stable Diffusion models.

## Tech Stack (Needs)

![Alt Text](./media/images/surprise-whats-in-the-box.gif)
The NeuroQuack tech stack is meticulously curated to provide a robust, scalable, and responsive user experience:
- **Frontend**: Cybernetic-themed UI, empowering users to craft their own visual journey.
- **AI**: Integration with a Large Language Model for engaging conversation and Stable Diffusion for dynamic image generation.
- **Cloud Infrastructure**: AWS SageMaker for deploying models, and Amazon S3 for data storage, all seamlessly orchestrated using Massdriver to streamline our infrastructure as code, ensuring quick, reliable, and repeatable deployments.
- **Networking**: Amazon Route53 for DNS management, providing a smooth and accessible user experience.
- **Security and Compliance**: Leveraging AWS IAM for robust access control, safeguarding user data and interactions.

## Brain Dump (Wants)

![Alt Text](./media/images/ThisIsFine.jpeg)

Future enhancements we're considering:
- Enhanced UI/UX for the IPython Notebook to make it even more immersive.
- Expanded LLM capabilities for richer conversations and more accurate prompt suggestions.
- Advanced image editing features post Stable Diffusion processing.
- Integration with additional AWS services for monitoring, logging, and automated deployment pipelines.

# Walkthrough
1) Set Environment Variables. Your bot Access Token can be found at https://twitchtokengenerator.com
   1) `export TWITCH_TOKEN=<<YOUR_BOT_ACCESS_TOKEN>>`
   2) `export INITIAL_CHANNELS=<<YOUR_CHANNEL_NAE>>`
2) Run `make docker_build`
3) Run `make docker_run`





## Backlog

![Alt Text](./media/images/dumpsterfire-dumpster.gif)

Here's what we're tackling next:
- Full mobile responsiveness for the IPython Notebook interface.
- Improved error handling and user feedback for image uploads and generation.
- Incorporation of user accounts and session management to save and retrieve past interactions.
- Enhanced analytics to understand user engagement and model performance.


## Working Examples:
    - SDXL
      - ECR: 763104351884.dkr.ecr.us-east-1.amazonaws.com/stabilityai-pytorch-inference:2.0.1-sgm0.1.0-gpu-py310-cu118-ubuntu20.04-sagemaker
      - S3: s3://jumpstart-cache-prod-us-east-1/stabilityai-infer/prepack/v1.0.1/infer-prepack-model-imagegeneration-stabilityai-stable-diffusion-xl-base-1-0.tar.gz
      - Instance Type: ml.g5.4xlarge

## Local Testing Commands:
  `uvicorn main:app --reload` to run FastAPI locally and reload with changes for testing