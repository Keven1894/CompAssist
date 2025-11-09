# Node.js Installation Guide

Complete guide for installing Node.js on Windows and Linux.

## Overview

Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine. It's essential for:
- Modern web development
- JavaScript tooling and build systems
- NPM package management
- Backend JavaScript applications

## Installation Options

### Native Installation vs Docker

| Aspect | Native Installation | Docker-based Node.js |
|--------|-------------------|---------------------|
| **Performance** | ✅ Faster | ⚠️ Slower (especially on Windows) |
| **OS Integration** | ✅ Full access | ❌ Limited (no Windows APIs) |
| **File Watching** | ✅ Works well | ⚠️ Requires polling on Windows |
| **Portability** | ❌ Platform-specific | ✅ Highly portable |
| **Setup Time** | 5-10 minutes | 2-5 minutes |
| **Best For** | Development, production | Testing, CI/CD, consistency |

**Recommendation**: Use **native installation** for development, **Docker** for standardized environments.

---

## Native Installation

### Windows Installation

#### Method 1: Using CompAssist (Automated)

The easiest way to install Node.js on Windows:

```bash
# Add to your config file (config/user_yourname.yaml)
software:
  packages:
    - name: nodejs
      manager: winget

# Run setup
python src/main.py setup --config config/user_yourname.yaml
```

#### Method 2: Using winget (Manual)

```powershell
# Install LTS version (recommended)
winget install OpenJS.NodeJS.LTS

# Or install current version
winget install OpenJS.NodeJS
```

#### Method 3: Official Installer

1. **Download**: https://nodejs.org/
   - **LTS** (Long Term Support) - Recommended for most users
   - **Current** - Latest features, less stable

2. **Run Installer**: `node-v*.msi`

3. **Installation Options**:
   - ✅ Automatically install necessary tools (Python, Visual Studio Build Tools)
   - ✅ Add to PATH
   - ✅ Install npm package manager

4. **Verify Installation**:
```powershell
node --version
npm --version
```

#### Method 4: Using Chocolatey

```powershell
# Install LTS
choco install nodejs-lts

# Or current version
choco install nodejs
```

### Linux Installation

#### Method 1: Using CompAssist (Automated)

```bash
# Add to config
software:
  packages:
    - name: nodejs
      manager: apt  # or yum, dnf

# Run setup
python src/main.py setup --config config/user_yourname.yaml
```

#### Method 2: Package Manager (Ubuntu/Debian)

```bash
# Using NodeSource repository (recommended for latest versions)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Or using default repository (older version)
sudo apt update
sudo apt install nodejs npm
```

#### Method 3: Package Manager (RHEL/Fedora)

```bash
# Fedora
sudo dnf install nodejs npm

# RHEL/CentOS (using NodeSource)
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo yum install nodejs
```

#### Method 4: Using nvm (Node Version Manager)

**Best for managing multiple Node.js versions:**

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell
source ~/.bashrc

# Install Node.js LTS
nvm install --lts

# Use specific version
nvm use --lts

# Set default version
nvm alias default node
```

### macOS Installation

#### Method 1: Using Homebrew

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node
```

#### Method 2: Official Installer

Download from https://nodejs.org/ and run the `.pkg` installer.

---

## Docker-based Node.js

For containerized Node.js workflows, especially useful for consistent environments across machines.

### Basic Docker Setup

```powershell
# Windows PowerShell
docker run -it --rm -v "${PWD}:/workspace" -w /workspace node:20 node --version
```

```bash
# Linux/macOS
docker run -it --rm -v "$(pwd):/workspace" -w /workspace node:20 node --version
```

### Docker Compose for Development

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  node-dev:
    image: node:20
    volumes:
      - ./:/workspace
      - node_modules:/workspace/node_modules  # Keep node_modules in volume
    working_dir: /workspace
    environment:
      - CHOKIDAR_USEPOLLING=1  # Enable file watching
    ports:
      - "3000:3000"
      - "5173:5173"  # Vite dev server
    command: bash
    stdin_open: true
    tty: true
```

**Usage:**
```bash
# Start container
docker-compose up -d node-dev

# Enter container
docker-compose exec node-dev bash

# Inside container
npm install
npm run dev
```

### Windows-Specific Docker Considerations

#### File Watching Issues

**Problem**: Hot reload doesn't work with bind mounts on Windows.

**Solution**: Use polling instead of native file watching:

```json
// package.json
{
  "scripts": {
    "dev": "CHOKIDAR_USEPOLLING=1 vite",
    "watch": "WATCHPACK_POLLING=true webpack --watch"
  }
}
```

**Or set environment variable:**
```yaml
# docker-compose.yml
environment:
  - CHOKIDAR_USEPOLLING=1
  - WATCHPACK_POLLING=true
```

#### Performance Optimization

**Problem**: Slow file I/O with bind mounts on Windows.

**Solutions:**

1. **Use named volumes for node_modules**:
```yaml
volumes:
  - ./:/workspace
  - node_modules:/workspace/node_modules  # Faster
```

2. **Don't share node_modules with host**:
```dockerfile
# .dockerignore
node_modules/
```

3. **Use WSL2** (Windows Subsystem for Linux):
   - Store code in WSL filesystem
   - Run Docker from WSL
   - Better performance than native Windows

#### Binary Compatibility

**Problem**: Linux-built native modules don't work on Windows host.

**Solution**: Build inside container, don't share `node_modules`:

```bash
# Build inside container
docker-compose run --rm node-dev npm install

# Run dev server
docker-compose up node-dev
```

#### Networking

**Problem**: Can't access `localhost` from host to container.

**Solution**: Use correct address:

```yaml
# In container, bind to 0.0.0.0 not localhost
"scripts": {
  "dev": "vite --host 0.0.0.0"
}
```

**Access from host:**
- Container → Host: Use `host.docker.internal`
- Host → Container: Use `localhost:<published-port>`

### Docker Best Practices

```yaml
# docker-compose.yml - Complete example
version: '3.8'

services:
  node-app:
    image: node:20-alpine  # Smaller image
    volumes:
      - ./:/app
      - node_modules:/app/node_modules
      - /app/node_modules/.cache  # Cache for faster builds
    working_dir: /app
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=1
      - WATCHPACK_POLLING=true
    ports:
      - "3000:3000"
      - "5173:5173"
    command: npm run dev
    restart: unless-stopped

volumes:
  node_modules:
```

**Key points:**
- Use Alpine for smaller image
- Named volume for `node_modules`
- Enable polling for file watching
- Expose necessary ports
- Use `restart: unless-stopped` for development

---

## Version Management

### Using nvm (Recommended for Development)

**Install nvm:**

```bash
# Linux/macOS
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Windows (using nvm-windows)
# Download from: https://github.com/coreybutler/nvm-windows/releases
```

**Common nvm commands:**

```bash
# List available versions
nvm ls-remote

# Install specific version
nvm install 18.17.0
nvm install 20.5.0

# Use specific version
nvm use 18.17.0

# Set default
nvm alias default 20.5.0

# List installed versions
nvm ls

# Check current version
nvm current
```

### Checking Installed Version

```bash
# Node.js version
node --version
node -v

# npm version
npm --version
npm -v

# Check installation paths
which node  # Linux/macOS
where node  # Windows

# Full info
node -p process.versions
```

---

## Post-Installation Setup

### Configure npm

```bash
# Set npm prefix (optional)
npm config set prefix ~/.npm-global

# Add to PATH (Linux/macOS)
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Update npm itself
npm install -g npm@latest
```

### Install Global Tools (Optional)

```bash
# Package manager alternative
npm install -g yarn pnpm

# Build tools
npm install -g typescript
npm install -g vite

# Linting and formatting
npm install -g eslint prettier

# Process manager
npm install -g pm2
```

### Verify with CompAssist

After installation, check with CompAssist:

```bash
python src/main.py check
```

Look for Node.js in the "Development Tools" section.

---

## Troubleshooting

### Node.js Not Found After Installation

**Windows:**
```powershell
# Check PATH
$env:PATH -split ";"

# Manually add to PATH (temporary)
$env:PATH += ";C:\Program Files\nodejs"

# Restart PowerShell
```

**Linux:**
```bash
# Check PATH
echo $PATH

# Add to PATH
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Permission Errors (Linux)

```bash
# Fix npm permissions
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Or use nvm (recommended)
```

### EACCES Errors on Windows

Run PowerShell as Administrator or configure npm prefix:

```powershell
npm config set prefix "$env:APPDATA\npm"
```

### Docker Issues

**Container can't access host services:**
```yaml
# Use host.docker.internal
environment:
  - API_URL=http://host.docker.internal:8000
```

**File watching not working:**
```yaml
environment:
  - CHOKIDAR_USEPOLLING=1
  - CHOKIDAR_INTERVAL=1000
```

**Slow performance on Windows:**
- Use WSL2
- Store code in WSL filesystem
- Use named volumes for dependencies

---

## When to Use Native vs Docker

### Use Native Node.js When:
- ✅ Primary development environment
- ✅ Need maximum performance
- ✅ Using Windows-specific APIs
- ✅ Working with USB/serial devices
- ✅ Building Electron apps
- ✅ Need native OS integration

### Use Docker Node.js When:
- ✅ Need consistent environment across team
- ✅ Testing on multiple Node versions
- ✅ CI/CD pipelines
- ✅ Deploying to containerized environments
- ✅ Sandboxed execution
- ✅ Quick version switching

### Use Both (Hybrid Approach):
- Native for primary development
- Docker for testing and deployment
- Docker for team consistency
- Native for performance-critical tasks

---

## Related Documentation

- **Docker Setup**: [docker-setup.md](../getting-started/docker-setup.md)
- **Configuration**: [/config/README.md](/config/README.md)
- **CompAssist Commands**: [/README.md](/README.md)

## External Resources

- [Node.js Official Site](https://nodejs.org/)
- [npm Documentation](https://docs.npmjs.com/)
- [nvm GitHub](https://github.com/nvm-sh/nvm)
- [nvm-windows](https://github.com/coreybutler/nvm-windows)
- [Docker Node.js Best Practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)

---

**Last Updated**: November 9, 2024  
**Applies To**: Windows 10+, Ubuntu 20.04+, macOS 10.15+


