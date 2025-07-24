#!/usr/bin/env python3
"""
WhatBot Deployment Script v1.2.0
Interactive CLI deployment tool for WhatBot WhatsApp automation platform

Author: Ben Adenle
Email: ben@techjamlabs.com
Phone: +2348099999928
Company: TECHJAMLABS Limited
"""

import os
import sys
import subprocess
import platform
import getpass
import json
import time
import shutil
from pathlib import Path

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

class WhatBotDeployer:
    def __init__(self):
        self.install_dir = "/opt/whatbot"
        self.pat_token = None
        self.deployment_config = {}
        
    def print_banner(self):
        banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    WhatBot Deployment Tool                   ║
║                        v1.2.0                               ║
║                                                              ║
║  WhatsApp Automation Platform - Enterprise Deployment       ║
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
    
    def run_command(self, command, check=True):
        try:
            subprocess.run(command, shell=True, check=check)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def check_system_requirements(self):
        self.print_step("SYSTEM CHECK", "Verifying system requirements...")
        
        # Check OS
        if platform.system().lower() != "linux":
            self.print_error("Unsupported operating system. WhatBot requires Linux.")
            return False
        
        # Check if running as root
        if os.geteuid() != 0:
            self.print_error("This script must be run as root (use sudo)")
            return False
        
        # Check disk space
        statvfs = os.statvfs('/')
        free_space_gb = (statvfs.f_frsize * statvfs.f_bavail) / (1024**3)
        if free_space_gb < 2:
            self.print_error(f"Insufficient disk space: {free_space_gb:.1f}GB available, 2GB required")
            return False
        self.print_success(f"Disk space: {free_space_gb:.1f}GB available")
        
        # Check required commands
        required_commands = ['git', 'curl', 'wget']
        for cmd in required_commands:
            if shutil.which(cmd) is None:
                self.print_error(f"Required command not found: {cmd}")
                return False
            self.print_success(f"Found: {cmd}")
        
        return True
    
    def get_pat_token(self):
        self.print_step("AUTHENTICATION", "Setting up repository access...")
        
        print(f"\n{Colors.OKCYAN}WhatBot is stored in a private repository that requires authentication.")
        print("You'll need a Personal Access Token (PAT) to access the repository.")
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
    
    def install_dependencies(self):
        self.print_step("DEPENDENCIES", "Installing system dependencies...")
        
        # Update package lists
        self.run_command("apt-get update")
        
        # Install packages
        packages = [
            'curl', 'wget', 'git', 'unzip', 'software-properties-common',
            'build-essential', 'postgresql', 'postgresql-contrib', 'nginx'
        ]
        
        for package in packages:
            if self.run_command(f"apt-get install -y {package}"):
                self.print_success(f"Installed: {package}")
            else:
                self.print_warning(f"Failed to install: {package}")
        
        # Install Node.js
        self.print_info("Installing Node.js 18.x...")
        self.run_command("curl -fsSL https://deb.nodesource.com/setup_18.x | bash -")
        self.run_command("apt-get install -y nodejs")
        
        # Install PM2
        self.run_command("npm install -g pm2")
        
        return True
    
    def setup_database(self):
        self.print_step("DATABASE", "Setting up PostgreSQL database...")
        
        # Start PostgreSQL
        self.run_command("systemctl start postgresql")
        self.run_command("systemctl enable postgresql")
        
        # Create database and user
        db_name = "whatbot_production"
        db_user = "whatbot_user"
        db_password = self.generate_secure_password()
        
        self.run_command(f"sudo -u postgres psql -c \"CREATE USER {db_user} WITH PASSWORD '{db_password}';\"")
        self.run_command(f"sudo -u postgres psql -c \"CREATE DATABASE {db_name} OWNER {db_user};\"")
        self.run_command(f"sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};\"")
        
        self.deployment_config['database'] = {
            'host': 'localhost',
            'port': 5432,
            'name': db_name,
            'user': db_user,
            'password': db_password
        }
        
        self.print_success("Database setup completed")
        return True
    
    def generate_secure_password(self, length=32):
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def clone_repository(self):
        self.print_step("REPOSITORY", "Cloning WhatBot repository...")
        
        os.makedirs(self.install_dir, exist_ok=True)
        os.chdir(self.install_dir)
        
        private_url = f"https://{self.pat_token}@github.com/TechJam-Labs/whatbot-master-copy.git"
        
        if self.run_command(f"git clone {private_url} ."):
            self.print_success("Repository cloned successfully")
            return True
        else:
            self.print_error("Failed to clone repository")
            return False
    
    def setup_environment(self):
        self.print_step("ENVIRONMENT", "Setting up environment configuration...")
        
        jwt_secret = self.generate_secure_password(64)
        
        env_content = f"""# WhatBot Environment Configuration
PORT=41100
NODE_ENV=production
BASE_URL=https://your-domain.com
JWT_SECRET={jwt_secret}
DB_HOST={self.deployment_config['database']['host']}
DB_PORT={self.deployment_config['database']['port']}
DB_NAME={self.deployment_config['database']['name']}
DB_USER={self.deployment_config['database']['user']}
DB_PASSWORD={self.deployment_config['database']['password']}
WHATSAPP_NUMBER=+2349157342656
COMPANY_NAME=Your Company Name
APP_TITLE=WhatBot
API_KEY_REQUIRED=true
API_KEY_HEADER=X-API-Key
"""
        
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            self.print_success("Environment file created")
            return True
        except Exception as e:
            self.print_error(f"Failed to create environment file: {e}")
            return False
    
    def install_node_dependencies(self):
        self.print_step("NODE DEPENDENCIES", "Installing Node.js dependencies...")
        
        if self.run_command("npm install"):
            self.print_success("Node.js dependencies installed")
            return True
        else:
            self.print_error("Failed to install Node.js dependencies")
            return False
    
    def setup_nginx(self):
        self.print_step("NGINX", "Setting up Nginx configuration...")
        
        nginx_config = f"""server {{
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {{
        proxy_pass http://localhost:41100;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }}

    location /public {{
        alias {self.install_dir}/public;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}

    location /uploads {{
        alias {self.install_dir}/uploads;
        expires 1d;
    }}
}}
"""
        
        try:
            with open('/etc/nginx/sites-available/whatbot', 'w') as f:
                f.write(nginx_config)
            
            self.run_command("ln -sf /etc/nginx/sites-available/whatbot /etc/nginx/sites-enabled/")
            self.run_command("rm -f /etc/nginx/sites-enabled/default")
            
            if self.run_command("nginx -t"):
                self.run_command("systemctl reload nginx")
                self.print_success("Nginx configuration applied")
                return True
            else:
                self.print_error("Nginx configuration test failed")
                return False
                
        except Exception as e:
            self.print_error(f"Failed to setup Nginx: {e}")
            return False
    
    def setup_firewall(self):
        self.print_step("FIREWALL", "Setting up firewall rules...")
        
        if not shutil.which('ufw'):
            self.run_command("apt-get install -y ufw")
        
        self.run_command("ufw default deny incoming")
        self.run_command("ufw default allow outgoing")
        self.run_command("ufw allow ssh")
        self.run_command("ufw allow 'Nginx Full'")
        self.run_command("ufw allow 41100")
        self.run_command("ufw --force enable")
        
        self.print_success("Firewall configured")
        return True
    
    def create_service(self):
        self.print_step("SERVICE", "Creating systemd service...")
        
        os.makedirs("/var/log/whatbot", exist_ok=True)
        
        service_content = f"""[Unit]
Description=WhatBot WhatsApp Automation Platform
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory={self.install_dir}
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production
StandardOutput=journal
StandardError=journal
SyslogIdentifier=whatbot

[Install]
WantedBy=multi-user.target
"""
        
        try:
            with open('/etc/systemd/system/whatbot.service', 'w') as f:
                f.write(service_content)
            
            self.run_command("systemctl daemon-reload")
            self.run_command("systemctl enable whatbot.service")
            
            self.print_success("Systemd service created")
            return True
        except Exception as e:
            self.print_error(f"Failed to create service: {e}")
            return False
    
    def setup_logging(self):
        self.print_step("LOGGING", "Setting up logging...")
        
        os.makedirs(f"{self.install_dir}/logs", exist_ok=True)
        
        logrotate_config = f"""{self.install_dir}/logs/*.log {{
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        systemctl reload whatbot.service
    endscript
}}
"""
        
        try:
            with open('/etc/logrotate.d/whatbot', 'w') as f:
                f.write(logrotate_config)
            
            self.print_success("Logging configured")
            return True
        except Exception as e:
            self.print_warning(f"Logging setup failed: {e}")
            return False
    
    def create_backup_script(self):
        self.print_step("BACKUP", "Creating backup script...")
        
        backup_script = f"""#!/bin/bash
BACKUP_DIR="/opt/backups/whatbot"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump {self.deployment_config['database']['name']} > $BACKUP_DIR/db_$DATE.sql
tar -czf $BACKUP_DIR/app_$DATE.tar.gz {self.install_dir}
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
echo "Backup completed: $DATE"
"""
        
        try:
            backup_path = f"{self.install_dir}/scripts/backup.sh"
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            with open(backup_path, 'w') as f:
                f.write(backup_script)
            
            self.run_command(f"chmod +x {backup_path}")
            self.run_command(f"(crontab -l 2>/dev/null; echo '0 2 * * * {backup_path}') | crontab -")
            
            self.print_success("Backup script created")
            return True
        except Exception as e:
            self.print_warning(f"Backup script failed: {e}")
            return False
    
    def start_service(self):
        self.print_step("STARTUP", "Starting WhatBot service...")
        
        if self.run_command("systemctl start whatbot.service"):
            self.print_success("WhatBot service started")
            return True
        else:
            self.print_error("Failed to start WhatBot service")
            return False
    
    def health_check(self):
        self.print_step("HEALTH CHECK", "Running health check...")
        
        time.sleep(5)
        
        result = subprocess.run(
            "curl -s http://localhost:41100/api/v1/status",
            shell=True, capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            self.print_success("WhatBot API is responding")
            return True
        else:
            self.print_warning("WhatBot API is not responding yet")
            return False
    
    def save_deployment_info(self):
        deployment_info = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'install_directory': self.install_dir,
            'database': self.deployment_config['database'],
            'services': {
                'whatbot': '/etc/systemd/system/whatbot.service',
                'nginx': '/etc/nginx/sites-available/whatbot'
            }
        }
        
        try:
            with open(f"{self.install_dir}/deployment-info.json", 'w') as f:
                json.dump(deployment_info, f, indent=2)
            self.print_success("Deployment info saved")
        except Exception as e:
            self.print_warning(f"Failed to save deployment info: {e}")
    
    def print_completion(self):
        completion = f"""
{Colors.OKGREEN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    Deployment Complete!                      ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}

{Colors.OKCYAN}WhatBot has been successfully deployed!

{Colors.BOLD}Next Steps:{Colors.ENDC}
1. Configure your domain name in Nginx
2. Set up SSL: certbot --nginx -d your-domain.com
3. Access: http://localhost:41100
4. Initialize WhatsApp connection
5. Edit {self.install_dir}/.env

{Colors.BOLD}Commands:{Colors.ENDC}
- Status: systemctl status whatbot.service
- Logs: journalctl -u whatbot.service -f
- Restart: systemctl restart whatbot.service

{Colors.BOLD}Support:{Colors.ENDC}
- Email: ben@techjamlabs.com
- Phone: +2348099999928

{Colors.WARNING}Keep your PAT secure!{Colors.ENDC}
"""
        print(completion)
    
    def deploy(self):
        self.print_banner()
        
        if not self.check_system_requirements():
            return False
        
        if not self.get_pat_token():
            return False
        
        if not self.install_dependencies():
            return False
        
        if not self.setup_database():
            return False
        
        if not self.clone_repository():
            return False
        
        if not self.setup_environment():
            return False
        
        if not self.install_node_dependencies():
            return False
        
        if not self.setup_nginx():
            return False
        
        if not self.setup_firewall():
            return False
        
        if not self.create_service():
            return False
        
        if not self.setup_logging():
            return False
        
        if not self.create_backup_script():
            return False
        
        if not self.start_service():
            return False
        
        if not self.health_check():
            self.print_warning("Health check failed, but deployment may be successful")
        
        self.save_deployment_info()
        self.print_completion()
        
        return True

def main():
    deployer = WhatBotDeployer()
    
    try:
        success = deployer.deploy()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Deployment interrupted{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main() 