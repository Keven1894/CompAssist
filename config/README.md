# Configuration Directory

Configuration files for the Local Computer Assistant.

## Overview

This directory contains YAML configuration files that define system behavior, software packages, and user preferences.

## Configuration Files

### `default.yaml`
**Default system configuration** - Used when no user-specific config is provided.

**Contains:**
- Platform settings (Windows/Linux)
- Default software packages
- System settings and thresholds
- Environment variables
- Problem detection thresholds

**Usage:**
```bash
# Uses default.yaml automatically if no config specified
python src/main.py setup
```

### `user_example.yaml`
**Template for user-specific configurations** - Example showing how to create custom configs.

**Use this to:**
- Define your own software packages
- Override default settings
- Customize environment variables
- Set personal preferences

**Usage:**
```bash
# Copy and customize
cp config/user_example.yaml config/user_myname.yaml

# Edit your config
notepad config/user_myname.yaml

# Use your config
python src/main.py setup --config config/user_myname.yaml
```

### User Configuration Files (`user_*.yaml`)
**Personal configurations** - Ignored by Git (except `user_example.yaml`).

**Naming convention:**
- `user_<identifier>.yaml`
- Example: `user_john.yaml`, `user_dev.yaml`

**Note:** All `user_*.yaml` files are gitignored except `user_example.yaml` to protect personal information.

## Configuration Structure

### Basic Structure

```yaml
platform:
  windows:
    enabled: true
  linux:
    enabled: false

packages:
  common:
    - name: package-name
      manager: winget  # or chocolatey, apt, yum, dnf
      optional: false

  development:
    - name: git
      manager: direct_download
      url: https://git-scm.com/download/win
      
environment:
  variables:
    VARIABLE_NAME: "value"
    
system:
  settings:
    auto_update: true
    
thresholds:
  disk_space_warning_gb: 20
  memory_usage_warning_percent: 85
```

### Package Definition

Packages can be defined as strings or objects:

**Simple string:**
```yaml
packages:
  common:
    - git
    - python
```

**Detailed object:**
```yaml
packages:
  common:
    - name: git
      manager: winget
      version: latest
      optional: false
      
    - name: docker
      manager: direct_download
      url: https://docker.com/download
      optional: true
```

### Package Managers

Supported package managers by platform:

**Windows:**
- `winget` - Windows Package Manager (recommended)
- `chocolatey` - Chocolatey Package Manager
- `direct_download` - Direct download and installation

**Linux:**
- `apt` - Debian/Ubuntu
- `yum` - RHEL/CentOS (older)
- `dnf` - Fedora/RHEL (modern)
- `direct_download` - Direct download

### Environment Variables

Define environment variables to be set:

```yaml
environment:
  variables:
    JAVA_HOME: "C:\\Program Files\\Java\\jdk-17"
    MAVEN_HOME: "C:\\tools\\maven"
    # These will be added to PATH automatically if they contain bin/
```

### System Settings

Control assistant behavior:

```yaml
system:
  settings:
    auto_update: true          # Auto-update packages
    confirm_before_install: true  # Ask before installing
    log_level: INFO           # DEBUG, INFO, WARNING, ERROR
    backup_config: true       # Backup before changes
```

### Thresholds

Set detection thresholds for problem diagnosis:

```yaml
thresholds:
  disk_space_warning_gb: 20        # Warn if < 20GB free
  disk_space_critical_gb: 10       # Critical if < 10GB free
  memory_usage_warning_percent: 85 # Warn if > 85% used
  memory_usage_critical_percent: 95  # Critical if > 95% used
  cpu_usage_warning_percent: 90    # Warn if > 90% used
```

## Creating Your Configuration

### Step 1: Copy Template
```bash
cp config/user_example.yaml config/user_yourusername.yaml
```

### Step 2: Edit Configuration
```bash
# Windows
notepad config/user_yourusername.yaml

# Linux
nano config/user_yourusername.yaml
```

### Step 3: Customize Packages
Add or remove packages based on your needs:
```yaml
packages:
  development:
    - git
    - python
    - nodejs
    - docker
    
  productivity:
    - vscode
    - slack
    - zoom
```

### Step 4: Test Configuration
```bash
# Check what would be installed
python src/main.py check

# Run setup with your config
python src/main.py setup --config config/user_yourusername.yaml
```

## Configuration Validation

The assistant validates configurations before use:

- **Required fields**: Checks for mandatory fields
- **Package format**: Validates package definitions
- **Manager availability**: Ensures package manager is installed
- **Syntax**: Validates YAML syntax

### Common Validation Errors

**Invalid YAML syntax:**
```
Error: Invalid YAML in config file
Fix: Check indentation and colons
```

**Unknown package manager:**
```
Error: Package manager 'xyz' not supported
Fix: Use winget, chocolatey, apt, yum, or dnf
```

**Missing required field:**
```
Error: Package missing 'name' field
Fix: Add name to package definition
```

## Best Practices

1. **Start from template**: Always copy `user_example.yaml`
2. **Version control**: Don't commit personal configs
3. **Document changes**: Add comments to explain custom settings
4. **Test first**: Use `check` command before `setup`
5. **Backup**: Keep backups of working configs
6. **Minimal changes**: Only override what you need
7. **Platform-specific**: Use platform flags for multi-OS configs

## Examples

### Minimal Configuration
```yaml
platform:
  windows:
    enabled: true

packages:
  common:
    - git
    - python
```

### Development Environment
```yaml
platform:
  windows:
    enabled: true

packages:
  development:
    - name: git
      manager: winget
    - name: python
      manager: winget
    - name: nodejs
      manager: winget
    - name: vscode
      manager: winget
      
environment:
  variables:
    EDITOR: "code"
```

### Multi-Platform Configuration
```yaml
platform:
  windows:
    enabled: true
    packages:
      - git
      - python
  
  linux:
    enabled: true
    packages:
      - git
      - python3
```

## Troubleshooting

### Config not found
```bash
# Check file exists
ls config/user_yourusername.yaml

# Use absolute path
python src/main.py setup --config "C:\full\path\to\config.yaml"
```

### Config not loading
```bash
# Validate YAML syntax online: yamllint.com
# Or use Python
python -c "import yaml; yaml.safe_load(open('config/user_yourusername.yaml'))"
```

### Package not installing
- Check package name is correct for your platform
- Verify package manager is installed
- Try different package manager
- Use direct_download as fallback

## Security

- **Never commit secrets**: Don't put passwords, API keys in configs
- **Use environment variables**: For sensitive data
- **Review before sharing**: Remove personal paths and usernames
- **Gitignore**: User configs are automatically ignored

## Related Documentation

- Setup Guide: `/docs/getting-started/installation.md`
- Package Management: `/docs/guides/`
- Default Configuration: `default.yaml`
- Template: `user_example.yaml`


