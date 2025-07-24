#!/usr/bin/env python3
"""
WhatBot Update System v1.2.0
Interactive CLI update tool for WhatBot WhatsApp automation platform

Author: Ben Adenle
Email: ben@techjamlabs.com
Phone: +2348099999928
Company: TECHJAMLABS Limited

This script provides version management, testing environments, and
seamless updates for WhatBot with versioned API endpoints.
"""

import os
import sys
import subprocess
import json
import time
import shutil
import re
from pathlib import Path
from typing import Dict, List, Optional
import getpass

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class WhatBotUpdater:
    def __init__(self):
        self.current_version = "v1"
        self.production_dir = "/opt/whatbot"
        self.test_base_dir = "/opt/whatbot-test"
        self.backup_dir = "/opt/whatbot-backups"
        self.pat_token = None
        self.update_config = {}
        
    def print_banner(self):
        banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    WhatBot Update System                     ║
║                        v1.2.0                               ║
║                                                              ║
║  Version Management & Testing Environment                    ║
║                                                              ║
║  Author: Ben Adenle                                          ║
║  Company: TECHJAMLABS Limited                               ║
║  Email: ben@techjamlabs.com                                 ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
        print(banner)
    
    def print_step(self, step, message):
        print(f"\n{Colors.OKBLUE}{Colors.BOLD}[{step}]{Colors.ENDC} {message}")
    
    def print_success(self, message):
        print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
    
    def print_warning(self, message):
        print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")
    
    def print_error(self, message):
        print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")
    
    def print_info(self, message):
        print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")
    
    def run_command(self, command, check=True, capture_output=False):
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, check=check, 
                                      capture_output=True, text=True)
                return result.returncode, result.stdout, result.stderr
            else:
                subprocess.run(command, shell=True, check=check)
                return 0, "", ""
        except subprocess.CalledProcessError as e:
            if capture_output:
                return e.returncode, e.stdout, e.stderr
            else:
                return e.returncode, "", ""
    
    def check_root_access(self):
        """Check if running as root"""
        if os.geteuid() != 0:
            self.print_error("This script must be run as root (use sudo)")
            return False
        return True
    
    def get_pat_token(self):
        """Get GitHub Personal Access Token"""
        self.print_step("AUTHENTICATION", "Setting up repository access...")
        
        print(f"\n{Colors.OKCYAN}You'll need a GitHub Personal Access Token to access the repository.")
        print("If you don't have a PAT, please contact your administrator.{Colors.ENDC}\n")
        
        while True:
            self.pat_token = getpass.getpass("Enter your GitHub Personal Access Token: ").strip()
            
            if not self.pat_token:
                self.print_error("Personal Access Token cannot be empty")
                continue
            
            # Test the token
            self.print_info("Testing repository access...")
            test_url = f"https://{self.pat_token}@github.com/TechJam-Labs/whatbot-master-copy.git"
            
            result = subprocess.run(
                f"git ls-remote {test_url} --heads main",
                shell=True, capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                self.print_success("Repository access verified successfully")
                return True
            else:
                self.print_error("Invalid Personal Access Token or insufficient permissions")
                retry = input("Would you like to try again? (y/n): ").lower().strip()
                if retry != 'y':
                    return False
    
    def get_current_version_info(self):
        """Get current version information"""
        self.print_step("VERSION CHECK", "Checking current version...")
        
        if not os.path.exists(self.production_dir):
            self.print_error(f"Production directory not found: {self.production_dir}")
            return None
        
        # Check package.json for version
        package_json_path = os.path.join(self.production_dir, "package.json")
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    current_version = package_data.get('version', '1.0.0')
                    self.print_success(f"Current version: {current_version}")
                    return current_version
            except Exception as e:
                self.print_warning(f"Could not read package.json: {e}")
        
        # Check git tag
        os.chdir(self.production_dir)
        result = self.run_command("git describe --tags --abbrev=0", capture_output=True)
        if result[0] == 0:
            current_version = result[1].strip()
            self.print_success(f"Current version (git tag): {current_version}")
            return current_version
        
        self.print_warning("Could not determine current version, assuming v1.0.0")
        return "v1.0.0"
    
    def get_available_versions(self):
        """Get available versions from repository"""
        self.print_step("VERSION DISCOVERY", "Checking available versions...")
        
        private_url = f"https://{self.pat_token}@github.com/TechJam-Labs/whatbot-master-copy.git"
        
        # Get all tags
        result = self.run_command(f"git ls-remote --tags {private_url}", capture_output=True)
        if result[0] != 0:
            self.print_error("Failed to fetch available versions")
            return []
        
        # Parse tags
        tags = []
        for line in result[1].split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) == 2:
                    tag = parts[1].replace('refs/tags/', '')
                    if tag.startswith('v'):
                        tags.append(tag)
        
        # Sort versions (simple sorting, assumes semantic versioning)
        tags.sort(key=lambda x: [int(y) for y in x[1:].split('.')])
        
        if tags:
            self.print_success(f"Found {len(tags)} versions: {', '.join(tags)}")
        else:
            self.print_warning("No version tags found")
        
        return tags
    
    def create_backup(self):
        """Create backup of current installation"""
        self.print_step("BACKUP", "Creating backup of current installation...")
        
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_path = f"{self.backup_dir}/whatbot_backup_{timestamp}"
        
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            
            # Create backup
            self.run_command(f"cp -r {self.production_dir} {backup_path}")
            
            # Backup database
            db_backup_path = f"{backup_path}_database.sql"
            self.run_command(f"pg_dump whatbot_production > {db_backup_path}")
            
            self.print_success(f"Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            self.print_error(f"Backup failed: {e}")
            return None
    
    def create_test_environment(self, version):
        """Create test environment for new version"""
        self.print_step("TEST ENVIRONMENT", f"Creating test environment for {version}...")
        
        test_dir = f"{self.test_base_dir}/{version}"
        test_port = self.get_test_port(version)
        
        try:
            # Create test directory
            os.makedirs(test_dir, exist_ok=True)
            
            # Clone repository to test directory
            private_url = f"https://{self.pat_token}@github.com/TechJam-Labs/whatbot-master-copy.git"
            self.run_command(f"git clone {private_url} {test_dir}")
            
            # Checkout specific version
            os.chdir(test_dir)
            self.run_command(f"git checkout {version}")
            
            # Create test environment file
            self.create_test_env_file(test_dir, test_port, version)
            
            # Install dependencies
            self.run_command("npm install")
            
            # Create test database
            self.create_test_database(version)
            
            # Create test service
            self.create_test_service(version, test_dir, test_port)
            
            self.print_success(f"Test environment created: {test_dir}")
            self.print_success(f"Test port: {test_port}")
            
            return test_dir, test_port
        except Exception as e:
            self.print_error(f"Failed to create test environment: {e}")
            return None, None
    
    def get_test_port(self, version):
        """Get test port for version"""
        # Extract version number and calculate port
        version_num = version.replace('v', '').replace('.', '')
        base_port = 41200
        port_offset = int(version_num) * 10
        return base_port + port_offset
    
    def create_test_env_file(self, test_dir, test_port, version):
        """Create environment file for test environment"""
        env_content = f"""# WhatBot Test Environment - {version}
PORT={test_port}
NODE_ENV=test
BASE_URL=http://localhost:{test_port}
JWT_SECRET=test_jwt_secret_{version}_{int(time.time())}

# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=whatbot_test_{version.replace('.', '_')}
DB_USER=whatbot_test_user
DB_PASSWORD=test_password_{version}_{int(time.time())}

# WhatsApp configuration
WHATSAPP_NUMBER=+2349157342656
COMPANY_NAME=WhatBot Test - {version}
APP_TITLE=WhatBot Test {version}

# API configuration
API_KEY_REQUIRED=true
API_KEY_HEADER=X-API-Key
API_VERSION={version}

# Logging
LOG_LEVEL=debug
LOG_FILE={test_dir}/logs/app.log
"""
        
        with open(f"{test_dir}/.env", 'w') as f:
            f.write(env_content)
    
    def create_test_database(self, version):
        """Create test database for version"""
        db_name = f"whatbot_test_{version.replace('.', '_')}"
        db_user = "whatbot_test_user"
        db_password = f"test_password_{version}_{int(time.time())}"
        
        # Create database and user
        self.run_command(f"sudo -u postgres psql -c \"CREATE USER {db_user} WITH PASSWORD '{db_password}';\"")
        self.run_command(f"sudo -u postgres psql -c \"CREATE DATABASE {db_name} OWNER {db_user};\"")
        self.run_command(f"sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};\"")
        
        self.print_success(f"Test database created: {db_name}")
    
    def create_test_service(self, version, test_dir, test_port):
        """Create systemd service for test environment"""
        service_name = f"whatbot-test-{version.replace('.', '-')}"
        
        service_content = f"""[Unit]
Description=WhatBot Test Environment - {version}
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory={test_dir}
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=test
Environment=PORT={test_port}
StandardOutput=journal
StandardError=journal
SyslogIdentifier={service_name}

[Install]
WantedBy=multi-user.target
"""
        
        service_file = f"/etc/systemd/system/{service_name}.service"
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        self.run_command("systemctl daemon-reload")
        self.run_command(f"systemctl enable {service_name}")
        
        self.print_success(f"Test service created: {service_name}")
    
    def update_api_routes(self, test_dir, version):
        """Update API routes to use versioned endpoints"""
        self.print_step("API ROUTES", f"Updating API routes for {version}...")
        
        # Find server.js or main app file
        server_file = os.path.join(test_dir, "server.js")
        if not os.path.exists(server_file):
            self.print_warning("Server file not found, skipping API route updates")
            return
        
        try:
            with open(server_file, 'r') as f:
                content = f.read()
            
            # Update API routes to use versioned endpoints
            version_num = version.replace('v', '')
            
            # Replace /api/v1 with /api/v{version_num}
            updated_content = re.sub(
                r'/api/v1',
                f'/api/v{version_num}',
                content
            )
            
            # Add version information to the app
            version_info = f"""
// Version information
app.locals.version = '{version}';
app.locals.apiVersion = 'v{version_num}';

// Version endpoint
app.get('/api/version', (req, res) => {{
    res.json({{
        version: '{version}',
        apiVersion: 'v{version_num}',
        timestamp: new Date().toISOString()
    }});
}});
"""
            
            # Insert version info before the last closing brace
            if 'app.listen' in updated_content:
                parts = updated_content.split('app.listen')
                if len(parts) > 1:
                    updated_content = parts[0] + version_info + '\napp.listen' + parts[1]
            
            with open(server_file, 'w') as f:
                f.write(updated_content)
            
            self.print_success(f"API routes updated for {version}")
        except Exception as e:
            self.print_error(f"Failed to update API routes: {e}")
    
    def start_test_environment(self, version):
        """Start test environment"""
        self.print_step("TEST STARTUP", f"Starting test environment for {version}...")
        
        service_name = f"whatbot-test-{version.replace('.', '-')}"
        
        if self.run_command(f"systemctl start {service_name}"):
            self.print_success(f"Test environment started: {service_name}")
            
            # Wait for service to be ready
            time.sleep(5)
            
            # Get test port
            test_port = self.get_test_port(version)
            
            # Test API endpoint
            result = subprocess.run(
                f"curl -s http://localhost:{test_port}/api/version",
                shell=True, capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                try:
                    version_info = json.loads(result.stdout)
                    self.print_success(f"Test API responding: {version_info}")
                except:
                    self.print_success("Test API responding")
            else:
                self.print_warning("Test API not responding yet")
            
            return True
        else:
            self.print_error(f"Failed to start test environment")
            return False
    
    def test_version(self, version, test_dir, test_port):
        """Run tests for the new version"""
        self.print_step("TESTING", f"Running tests for {version}...")
        
        os.chdir(test_dir)
        
        # Run npm tests if available
        if os.path.exists("package.json"):
            package_data = json.load(open("package.json"))
            if "scripts" in package_data and "test" in package_data["scripts"]:
                self.print_info("Running npm tests...")
                result = self.run_command("npm test", check=False)
                if result[0] == 0:
                    self.print_success("NPM tests passed")
                else:
                    self.print_warning("NPM tests failed")
        
        # Test API endpoints
        self.print_info("Testing API endpoints...")
        
        endpoints_to_test = [
            f"http://localhost:{test_port}/api/version",
            f"http://localhost:{test_port}/api/v{version.replace('v', '')}/status",
            f"http://localhost:{test_port}/api/v{version.replace('v', '')}/health"
        ]
        
        for endpoint in endpoints_to_test:
            result = subprocess.run(
                f"curl -s {endpoint}",
                shell=True, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                self.print_success(f"✓ {endpoint}")
            else:
                self.print_warning(f"⚠ {endpoint}")
        
        self.print_success(f"Testing completed for {version}")
    
    def prompt_for_production_update(self, version):
        """Prompt user for production update"""
        self.print_step("PRODUCTION UPDATE", f"Ready to update production to {version}")
        
        print(f"\n{Colors.OKCYAN}Test environment is running successfully.")
        print(f"You can test the new version at: http://localhost:{self.get_test_port(version)}")
        print(f"API endpoints: /api/v{version.replace('v', '')}/")
        print(f"\nWould you like to update production to {version}?{Colors.ENDC}\n")
        
        while True:
            choice = input("Update production? (y/n/test): ").lower().strip()
            
            if choice == 'y':
                return 'update'
            elif choice == 'n':
                return 'skip'
            elif choice == 'test':
                return 'test'
            else:
                print("Please enter 'y' for update, 'n' to skip, or 'test' to continue testing")
    
    def update_production(self, version):
        """Update production to new version"""
        self.print_step("PRODUCTION UPDATE", f"Updating production to {version}...")
        
        # Stop production service
        self.run_command("systemctl stop whatbot.service")
        
        # Backup current production
        backup_path = self.create_backup()
        
        try:
            # Update production directory
            os.chdir(self.production_dir)
            
            # Fetch latest changes
            self.run_command("git fetch --all")
            
            # Checkout new version
            self.run_command(f"git checkout {version}")
            
            # Update dependencies
            self.run_command("npm install")
            
            # Update API routes
            self.update_api_routes(self.production_dir, version)
            
            # Update environment file
            self.update_production_env(version)
            
            # Start production service
            self.run_command("systemctl start whatbot.service")
            
            # Wait for service to be ready
            time.sleep(5)
            
            # Test production
            result = subprocess.run(
                "curl -s http://localhost:41100/api/version",
                shell=True, capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                self.print_success("Production updated successfully")
                return True
            else:
                self.print_error("Production update failed")
                return False
                
        except Exception as e:
            self.print_error(f"Production update failed: {e}")
            
            # Restore from backup
            if backup_path:
                self.print_info("Restoring from backup...")
                self.run_command(f"rm -rf {self.production_dir}")
                self.run_command(f"cp -r {backup_path} {self.production_dir}")
                self.run_command("systemctl start whatbot.service")
            
            return False
    
    def update_production_env(self, version):
        """Update production environment file"""
        env_file = os.path.join(self.production_dir, ".env")
        
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                content = f.read()
            
            # Update version-related variables
            content = re.sub(r'APP_TITLE=.*', f'APP_TITLE=WhatBot {version}', content)
            content = re.sub(r'API_VERSION=.*', f'API_VERSION={version}', content)
            
            with open(env_file, 'w') as f:
                f.write(content)
    
    def cleanup_test_environment(self, version):
        """Clean up test environment"""
        self.print_step("CLEANUP", f"Cleaning up test environment for {version}...")
        
        service_name = f"whatbot-test-{version.replace('.', '-')}"
        test_dir = f"{self.test_base_dir}/{version}"
        
        # Stop and disable service
        self.run_command(f"systemctl stop {service_name}")
        self.run_command(f"systemctl disable {service_name}")
        
        # Remove service file
        service_file = f"/etc/systemd/system/{service_name}.service"
        if os.path.exists(service_file):
            os.remove(service_file)
        
        # Remove test directory
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        
        # Remove test database
        db_name = f"whatbot_test_{version.replace('.', '_')}"
        self.run_command(f"sudo -u postgres psql -c \"DROP DATABASE IF EXISTS {db_name};\"")
        
        self.run_command("systemctl daemon-reload")
        self.print_success("Test environment cleaned up")
    
    def show_update_summary(self, version, test_port):
        """Show update summary"""
        summary = f"""
{Colors.OKGREEN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    Update Summary                            ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}

{Colors.OKCYAN}WhatBot has been updated successfully!

{Colors.BOLD}Version Information:{Colors.ENDC}
- New Version: {version}
- API Version: v{version.replace('v', '')}
- Production: http://localhost:41100
- Test Environment: http://localhost:{test_port}

{Colors.BOLD}API Endpoints:{Colors.ENDC}
- Production: /api/v{version.replace('v', '')}/
- Test: /api/v{version.replace('v', '')}/
- Version Info: /api/version

{Colors.BOLD}Service Management:{Colors.ENDC}
- Production: systemctl status whatbot.service
- Test: systemctl status whatbot-test-{version.replace('.', '-')}.service

{Colors.BOLD}Useful Commands:{Colors.ENDC}
- View logs: journalctl -u whatbot.service -f
- Restart: systemctl restart whatbot.service
- Test API: curl http://localhost:41100/api/version

{Colors.BOLD}Next Steps:{Colors.ENDC}
1. Test the new version thoroughly
2. Monitor logs for any issues
3. Update documentation if needed
4. Clean up test environment when ready

{Colors.WARNING}Remember to backup your data regularly!{Colors.ENDC}
"""
        print(summary)
    
    def update(self):
        """Main update process"""
        self.print_banner()
        
        if not self.check_root_access():
            return False
        
        if not self.get_pat_token():
            return False
        
        # Get current version
        current_version = self.get_current_version_info()
        if not current_version:
            return False
        
        # Get available versions
        available_versions = self.get_available_versions()
        if not available_versions:
            self.print_error("No versions available for update")
            return False
        
        # Show available versions
        print(f"\n{Colors.BOLD}Available versions:{Colors.ENDC}")
        for i, version in enumerate(available_versions, 1):
            if version == current_version:
                print(f"{i}. {version} (current)")
            else:
                print(f"{i}. {version}")
        
        # Let user select version
        while True:
            try:
                choice = input(f"\nSelect version to update to (1-{len(available_versions)}): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(available_versions):
                    target_version = available_versions[choice_idx]
                    break
                else:
                    print("Invalid selection")
            except ValueError:
                print("Please enter a valid number")
        
        if target_version == current_version:
            self.print_info("Already on the selected version")
            return True
        
        # Create backup
        backup_path = self.create_backup()
        if not backup_path:
            self.print_warning("Backup failed, but continuing...")
        
        # Create test environment
        test_dir, test_port = self.create_test_environment(target_version)
        if not test_dir:
            return False
        
        # Update API routes
        self.update_api_routes(test_dir, target_version)
        
        # Start test environment
        if not self.start_test_environment(target_version):
            return False
        
        # Run tests
        self.test_version(target_version, test_dir, test_port)
        
        # Prompt for production update
        update_choice = self.prompt_for_production_update(target_version)
        
        if update_choice == 'update':
            if self.update_production(target_version):
                self.show_update_summary(target_version, test_port)
                
                # Ask if user wants to clean up test environment
                cleanup = input("\nClean up test environment? (y/n): ").lower().strip()
                if cleanup == 'y':
                    self.cleanup_test_environment(target_version)
                
                return True
            else:
                return False
        elif update_choice == 'test':
            self.print_info(f"Test environment remains active at http://localhost:{test_port}")
            self.print_info("You can continue testing and update production later")
            return True
        else:
            self.print_info("Update cancelled")
            self.cleanup_test_environment(target_version)
            return True

def main():
    updater = WhatBotUpdater()
    
    try:
        success = updater.update()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Update interrupted{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main() 