# Environment Variable Setup Guide

This guide shows you how to securely store your access tokens so they're hidden when streaming.

## Quick Reference: TTG Tokens Format

When you get tokens from Twitch Token Generator (TTG), you'll receive:
- `ACCESS_TOKEN` → Use this as `twitch_token` in `/configure`
- `REFRESH_TOKEN` → Store for future use
- `CLIENT_ID` → Store for future use

**For PowerShell Profile, add:**
```powershell
$env:TWITCH_ACCESS_TOKEN="your_access_token_here"
$env:TWITCH_REFRESH_TOKEN="your_refresh_token_here"
$env:TWITCH_CLIENT_ID="your_client_id_here"
```

**For `/configure` endpoint, use:**
```json
{
  "twitch": {
    "twitch_token": "your_access_token_here",
    "initial_channels": "DuckTapeDevOps"
  }
}
```

## Development Environment Setup

This project uses **uv** as the Python package manager for cross-platform compatibility (Windows, Linux, macOS). `uv` automatically handles virtual environments and works identically across all platforms, solving the Windows/Linux path differences.

### Installing uv

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Alternative (using pip):**
```bash
pip install uv
```

**Verify installation:**
```bash
uv --version
```

### Using uv for Development

The project uses `pyproject.toml` for dependency management. All `just` commands automatically use `uv`:

**Setup virtual environment and install dependencies:**
```bash
just venv-setup
# Or manually: cd app && uv sync
```

**Run the bot:**
```bash
just run-fast
# Or manually: cd app && uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Add a new dependency:**
```bash
cd app
uv add package-name
```

**Update dependencies:**
```bash
cd app
uv sync
```

**Benefits of uv:**
- ✅ **Cross-platform**: Same commands work on Windows, Linux, macOS
- ✅ **No manual venv activation**: `uv run` automatically uses the project environment
- ✅ **10-100x faster** than pip/Poetry for dependency resolution
- ✅ **Modern standard**: Uses `pyproject.toml` (PEP 518/621)

**Cross-Platform Compatibility:**
- The `justfile` is configured for Windows PowerShell, but all `uv` commands work identically on Linux and macOS
- On Linux/macOS, you can use the same `just` commands, or run `uv` commands directly:
  ```bash
  cd app
  uv sync
  uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  ```
- `uv` automatically handles the difference between Windows (`venv\Scripts\`) and Unix (`venv/bin/`) paths

## Windows Options

### Option 1: PowerShell Profile (Recommended for Windows PowerShell)

Since you're on Windows using PowerShell, this is the best option. Add to your PowerShell profile:

```powershell
# NeuroQuack Bot Configuration
$env:REPLICATE_API_TOKEN="r8_your_token_here"
$env:REPLICATE_ORG="ducktapedevops"
$env:BOT_NAME="Ducktronaut"

# Twitch Token Generator (TTG) Credentials
# Get these from: https://twitchtokengenerator.com/
$env:TWITCH_ACCESS_TOKEN="your_access_token_here"
$env:TWITCH_REFRESH_TOKEN="your_refresh_token_here"
$env:TWITCH_CLIENT_ID="your_client_id_here"

# Note: For the /configure endpoint, use TWITCH_ACCESS_TOKEN as the twitch_token value
# You can optionally prefix with "oauth:" if needed: "oauth:$env:TWITCH_ACCESS_TOKEN"

# Optional: Model Overrides
# $env:MODEL_PHOTOMAKER="jd7h/photomaker:latest"
# $env:MODEL_CLIP_INTERROGATOR="pharmapsychotic/clip-interrogator:8151e1c9f47e696fa316146a2e35812ccf79cfc9eba05b11c7f450155102af70"
# $env:MODEL_SDXL="stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc"
# $env:MODEL_BLIP="ducktapedevops/blip"
```

**Find your profile location:**
```powershell
$PROFILE
```

**Edit your profile:**
```powershell
notepad $PROFILE
```

**If the file doesn't exist, create it:**
```powershell
New-Item -Path $PROFILE -Type File -Force
notepad $PROFILE
```

**To reload:**
```powershell
. $PROFILE
```

**To verify:**
```powershell
$env:REPLICATE_API_TOKEN
```

### Option 2: System Environment Variables (Windows - Permanent)

For system-wide environment variables that persist across sessions:

1. Open **System Properties**:
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Or: Settings → System → About → Advanced system settings

2. Click **Environment Variables**

3. Under **User variables**, click **New** and add:
   - `REPLICATE_API_TOKEN` = `r8_your_token_here`
   - `REPLICATE_ORG` = `ducktapedevops`
   - `BOT_NAME` = `Ducktronaut`

4. Click **OK** on all dialogs

5. **Restart your terminal/PowerShell** for changes to take effect

**Note:** These are visible in System Properties, so be careful not to show that on stream.

### Option 3: Git Bash Profile (If using Git Bash)

If you use Git Bash on Windows, add to `~/.bashrc` or `~/.bash_profile`:

```bash
# NeuroQuack Bot Configuration
export REPLICATE_API_TOKEN="r8_your_token_here"
export REPLICATE_ORG="ducktapedevops"
export BOT_NAME="Ducktronaut"

# Twitch Token Generator (TTG) Credentials
export TWITCH_ACCESS_TOKEN="your_access_token_here"
export TWITCH_REFRESH_TOKEN="your_refresh_token_here"
export TWITCH_CLIENT_ID="your_client_id_here"
```

**To apply:**
```bash
source ~/.bashrc
```

### Option 4: WSL (If using Windows Subsystem for Linux)

If you're using WSL, add to `~/.bashrc` (bash) or `~/.zshrc` (zsh):

```bash
# NeuroQuack Bot Configuration
export REPLICATE_API_TOKEN="r8_your_token_here"
export REPLICATE_ORG="ducktapedevops"
export BOT_NAME="Ducktronaut"

# Twitch Token Generator (TTG) Credentials
export TWITCH_ACCESS_TOKEN="your_access_token_here"
export TWITCH_REFRESH_TOKEN="your_refresh_token_here"
export TWITCH_CLIENT_ID="your_client_id_here"
```

**To apply:**
```bash
source ~/.bashrc  # or source ~/.zshrc
```

## Cross-Platform Options

### Option 5: Using `.env` File (Recommended for Docker)

Create a `.env` file in the project root:

```bash
# Required: Replicate API Configuration
REPLICATE_API_TOKEN=r8_your_token_here
REPLICATE_ORG=ducktapedevops

# Required: Twitch Bot Configuration
BOT_NAME=Ducktronaut

# Twitch Token Generator (TTG) Credentials
# Get these from: https://twitchtokengenerator.com/
TWITCH_ACCESS_TOKEN=your_access_token_here
TWITCH_REFRESH_TOKEN=your_refresh_token_here
TWITCH_CLIENT_ID=your_client_id_here

# Note: For the /configure endpoint, use TWITCH_ACCESS_TOKEN as the twitch_token value
# Format: "oauth:TWITCH_ACCESS_TOKEN" or just "TWITCH_ACCESS_TOKEN" (TwitchIO handles both)

# Optional: Model Overrides (defaults are in Dockerfile)
# MODEL_PHOTOMAKER=jd7h/photomaker:latest
# MODEL_CLIP_INTERROGATOR=pharmapsychotic/clip-interrogator:8151e1c9f47e696fa316146a2e35812ccf79cfc9eba05b11c7f450155102af70
# MODEL_SDXL=stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc
# MODEL_BLIP=ducktapedevops/blip
```

**Note:** `.env` is already in `.gitignore`, so it won't be committed to git.

The `just docker-run` command will automatically use this `.env` file.

**Note:** `.env` is already in `.gitignore`, so it won't be committed to git.

### Option 6: Using `.zshrc` (Mac/Linux/WSL with zsh)

If you're using zsh (Mac, Linux, or WSL), add to your `~/.zshrc` file:

```bash
# NeuroQuack Bot Configuration
export REPLICATE_API_TOKEN="r8_your_token_here"
export REPLICATE_ORG="ducktapedevops"
export BOT_NAME="Ducktronaut"

# Twitch Token Generator (TTG) Credentials
export TWITCH_ACCESS_TOKEN="your_access_token_here"
export TWITCH_REFRESH_TOKEN="your_refresh_token_here"
export TWITCH_CLIENT_ID="your_client_id_here"
```

**To apply:**
```bash
source ~/.zshrc
```

**To verify:**
```bash
echo $REPLICATE_API_TOKEN
```

## Which Option Should I Use?

**For Windows PowerShell (Most Common):**
- Use **Option 1: PowerShell Profile** - Best for keeping tokens in your user directory, hidden from stream

**For Docker:**
- Use **Option 5: `.env` File** - Simplest for Docker, automatically loaded

**For System-Wide (All Apps):**
- Use **Option 2: System Environment Variables** - Works for all applications, but visible in System Properties

**For Git Bash:**
- Use **Option 3: Git Bash Profile**

**For WSL:**
- Use **Option 4: WSL Profile** (bashrc or zshrc)

## Security Notes

- ✅ **DO NOT** commit `.env` files or tokens to git (`.env` is already in `.gitignore`)
- ✅ **DO NOT** show your PowerShell profile, `.zshrc`, `.bashrc`, or System Properties on stream
- ✅ Use the `/configure` endpoint for runtime configuration if you prefer
- ✅ Consider using a password manager to store tokens securely
- ✅ PowerShell profile location is usually: `Documents\PowerShell\Microsoft.PowerShell_profile.ps1`

## Getting Your Tokens

1. **Replicate API Token**: https://replicate.com/account/api-tokens
2. **Replicate Org**: Your organization name on Replicate (e.g., "ducktapedevops")
3. **Twitch Tokens (TTG)**: https://twitchtokengenerator.com/
   - **ACCESS_TOKEN**: Use this as `twitch_token` in the `/configure` endpoint
   - **REFRESH_TOKEN**: For refreshing the access token (currently not used in code, but good to keep)
   - **CLIENT_ID**: Your Twitch application client ID (currently not used in code, but good to keep)
4. **BOT_NAME**: Your Twitch bot's username (e.g., "Ducktronaut")

## Using the Configure Endpoint

If you prefer to configure via API instead of environment variables:

1. Start the bot: `just run-fast` (works on Windows/Linux/macOS) or `just docker-run`
2. POST to `http://localhost:8000/configure` (or `http://localhost:8080/configure` for Docker):

```json
{
  "api": {
    "replicate_token": "r8_your_token_here",
    "replicate_org": "ducktapedevops"
  },
  "twitch": {
    "twitch_token": "itcy6xudifdg7bjqzowwq52ph1542t",
    "initial_channels": "DuckTapeDevOps"
  }
}
```

**Using TTG Tokens:**
- Use your `ACCESS_TOKEN` from TTG as the `twitch_token` value
- You can use it directly or with `oauth:` prefix (e.g., `"oauth:your_token"`)
- TwitchIO library handles both formats

**Example:**
```json
{
  "api": {
    "replicate_token": "r8_your_token_here",
    "replicate_org": "ducktapedevops"
  },
  "twitch": {
    "twitch_token": "your_access_token_here",
    "initial_channels": "DuckTapeDevOps"
  }
}
```

**Note:** 
- You still need `BOT_NAME` as an environment variable for Twitch bot commands to work
- The `REFRESH_TOKEN` and `CLIENT_ID` from TTG are not currently used by the bot, but keep them stored in case you need them later
