# LLM Hub Installation Guide

This guide provides step-by-step instructions for installing and setting up LLM Hub on Windows.

## Prerequisites

Before installing LLM Hub, ensure you have the following software installed:

### Required Software

1. **Windows 10 or Windows 11**
   - 64-bit version required
   - Administrator privileges for Docker installation

2. **Docker Desktop for Windows**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Minimum 4GB RAM recommended
   - WSL2 backend enabled (recommended)

3. **LM Studio**
   - Download from: https://lmstudio.ai/
   - Any recent version with local server support
   - At least one language model downloaded

### Optional Software

- **Git for Windows** (if cloning from repository)
- **Visual Studio Code** (for development)
- **Windows Terminal** (improved command line experience)

## Installation Steps

### Step 1: Install Docker Desktop

1. **Download Docker Desktop**
   - Visit https://www.docker.com/products/docker-desktop/
   - Click "Download for Windows"
   - Save the installer file

2. **Run the Installer**
   - Double-click the downloaded installer
   - Follow the installation wizard
   - Accept the license agreement
   - Choose installation options (default settings recommended)

3. **Configure Docker Desktop**
   - Launch Docker Desktop from Start Menu
   - Complete the initial setup wizard
   - Sign in to Docker Hub (optional but recommended)
   - Enable WSL2 backend if prompted

4. **Verify Docker Installation**
   ```cmd
   docker --version
   docker-compose --version
   ```

### Step 2: Install and Configure LM Studio

1. **Download LM Studio**
   - Visit https://lmstudio.ai/
   - Download the Windows installer
   - Run the installer and follow the setup wizard

2. **Download a Language Model**
   - Launch LM Studio
   - Browse the model library
   - Download a model (e.g., Llama 2 7B Chat)
   - Wait for download to complete

3. **Enable Local Server**
   - In LM Studio, go to Settings
   - Find "Local Server" section
   - Enable "Start server automatically"
   - Set port to 1234 (default)
   - Load your downloaded model

4. **Verify LM Studio Server**
   ```cmd
   curl http://localhost:1234/v1/models
   ```
   You should see a JSON response with available models.

### Step 3: Download LLM Hub

#### Option A: Download Release (Recommended)
1. Visit the project releases page
2. Download the latest release ZIP file
3. Extract to your desired location (e.g., `C:\llm-hub`)

#### Option B: Clone Repository
```cmd
git clone https://github.com/your-org/llm-hub.git
cd llm-hub
```

### Step 4: Configure Environment

1. **Navigate to Project Directory**
   ```cmd
   cd C:\llm-hub
   ```

2. **Copy Environment Template**
   ```cmd
   copy ops\compose\.env.example ops\compose\.env
   ```

3. **Edit Configuration (Optional)**
   - Open `ops\compose\.env` in a text editor
   - Modify settings if needed (defaults work for most setups)
   - Key settings:
     ```
     API_KEY=your_secure_api_key_here
     LM_STUDIO_URL=http://host.docker.internal:1234
     GATEWAY_PORT=8080
     ```

### Step 5: Start LLM Hub

1. **Launch Services**
   ```cmd
   start.bat
   ```

2. **Wait for Startup**
   - The script will start Docker containers
   - Wait for health checks to pass
   - Services should be ready in 1-2 minutes

3. **Verify Installation**
   - Gateway: http://localhost:8080/health
   - Bridge: http://localhost:3000/health
   - Check that both return healthy status

### Step 6: Test the Installation

1. **Run Test Suite**
   ```cmd
   cd ops\scripts
   bash run-all-tests.sh
   ```

2. **Manual Verification**
   ```cmd
   # Check available tools
   curl -H "Authorization: Bearer changeme" http://localhost:8080/mcp/tools

   # Test inference
   curl -X POST -H "Authorization: Bearer changeme" -H "Content-Type: application/json" ^
        -d "{\"parameters\":{\"prompt\":\"Hello\",\"model\":\"your-model-name\"}}" ^
        http://localhost:8080/tools/inference
   ```

## Post-Installation Configuration

### Security Configuration

1. **Change Default API Key**
   - Edit `ops\compose\.env`
   - Set a strong, unique API key:
     ```
     API_KEY=your_very_secure_random_key_here
     ```

2. **Restart Services**
   ```cmd
   stop.bat
   start.bat
   ```

### Performance Tuning

1. **Adjust Docker Resources**
   - Open Docker Desktop settings
   - Go to Resources → Advanced
   - Increase memory allocation (8GB+ recommended)
   - Increase CPU allocation if available

2. **Configure Rate Limits**
   - Edit `ops\compose\.env`
   - Adjust rate limiting:
     ```
     RATE_LIMIT_PER_MINUTE=120
     ```

### Firewall Configuration

1. **Windows Firewall**
   - Docker Desktop should automatically configure firewall rules
   - If issues persist, manually allow Docker Desktop through firewall

2. **Antivirus Configuration**
   - Add Docker Desktop to antivirus exclusions
   - Add project directory to exclusions

## Troubleshooting

### Common Issues

1. **Docker Not Starting**
   - Ensure virtualization is enabled in BIOS
   - Check Windows features: Hyper-V, WSL2
   - Restart computer after Docker installation

2. **Port Conflicts**
   - Check if ports 8080, 3000, or 1234 are in use
   - Change ports in `.env` file if needed
   - Restart services after changes

3. **LM Studio Connection Issues**
   - Verify LM Studio server is running
   - Check firewall settings
   - Ensure model is loaded in LM Studio

4. **Permission Issues**
   - Run command prompt as Administrator
   - Check Docker Desktop permissions
   - Verify file permissions in project directory

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review Docker Desktop logs
3. Check service logs: `docker-compose logs`
4. Create an issue with detailed error information

## Next Steps

After successful installation:

1. Read the [Configuration Guide](CONFIGURATION.md) for advanced settings
2. Explore the [API Documentation](api/MCP-ENDPOINTS.md) for integration
3. Review the [Development Guide](DEVELOPMENT.md) for customization
4. Set up monitoring and logging for production use

## Uninstallation

To completely remove LLM Hub:

1. **Stop Services**
   ```cmd
   stop.bat
   ```

2. **Remove Containers and Images**
   ```cmd
   docker-compose down --rmi all --volumes
   docker system prune -a
   ```

3. **Delete Project Directory**
   - Remove the entire LLM Hub folder
   - Clean up any shortcuts or desktop icons

4. **Optional: Uninstall Docker Desktop**
   - Use Windows Add/Remove Programs
   - Remove Docker Desktop if no longer needed
