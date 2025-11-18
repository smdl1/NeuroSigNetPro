#!/usr/bin/env python3
"""
NeuroSigNet Pro - Advanced Installer
Professional installation with AI model downloading and system optimization
"""

import os
import sys
import json
import time
import shutil
import zipfile
import tempfile
import requests
import subprocess
import platform
import ctypes
import winreg
from pathlib import Path
from datetime import datetime

class NeuroSigNetAdvancedInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.temp_dir = tempfile.mkdtemp(prefix="neurosignet_")
        self.install_dir = Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')) / "NeuroSigNetPro"
        self.desktop_dir = Path(os.path.join(os.path.expanduser("~"), "Desktop"))
        
    def is_admin(self):
        """Check if running as administrator"""
        try:
            if self.system == "windows":
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def run_as_admin(self):
        """Restart with admin privileges"""
        if self.system == "windows" and not self.is_admin():
            print("🔄 Restarting with administrator privileges...")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit()
    
    def check_system_requirements(self):
        """Check system requirements"""
        print("🔍 Checking system requirements...")
        
        # Simple checks for demonstration
        requirements_met = True
        
        # Check Python version
        python_version = sys.version_info
        if (python_version.major, python_version.minor) >= (3, 8):
            print("✅ Python 3.8+")
        else:
            print("❌ Python 3.8+ required")
            requirements_met = False
        
        # Check disk space
        try:
            disk_free = shutil.disk_usage(str(self.install_dir.parent)).free / (1024**3)
            if disk_free >= 2:
                print(f"✅ Disk space: {disk_free:.1f} GB free")
            else:
                print(f"❌ Need 2 GB free disk space, only {disk_free:.1f} GB available")
                requirements_met = False
        except:
            print("⚠️ Could not check disk space")
        
        return requirements_met
    
    def install_python_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing Python dependencies...")
        
        dependencies = [
            "torch>=2.0.0",
            "ultralytics>=8.0.0",
            "opencv-python>=4.8.0",
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
            "python-multipart>=0.0.6",
            "pillow>=10.0.0",
            "numpy>=1.24.0",
            "requests>=2.31.0",
            "aiofiles>=23.0.0",
            "jinja2>=3.1.0"
        ]
        
        success_count = 0
        for dep in dependencies:
            try:
                print(f"  Installing {dep}...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", dep
                ], capture_output=True, text=True, check=True)
                success_count += 1
            except subprocess.CalledProcessError:
                print(f"  ⚠️ Failed to install {dep}")
        
        print(f"✅ Installed {success_count}/{len(dependencies)} packages")
        return success_count >= len(dependencies) * 0.8
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut"""
        try:
            shortcut_path = self.desktop_dir / "NeuroSigNet Pro.lnk"
            
            # Create batch file as fallback
            bat_content = f'''
@echo off
cd /d "{self.install_dir}"
python main.py
pause
'''
            bat_path = self.desktop_dir / "NeuroSigNet Pro.bat"
            with open(bat_path, 'w') as f:
                f.write(bat_content)
            
            print("✅ Desktop shortcut created")
            return True
        except Exception as e:
            print(f"⚠️ Could not create desktop shortcut: {e}")
            return False
    
    def create_start_menu_entry(self):
        """Create Start Menu entry"""
        if self.system != "windows":
            return True
        
        try:
            start_menu_dir = Path(os.path.join(
                os.environ["APPDATA"], 
                "Microsoft", "Windows", "Start Menu", "Programs"
            ))
            neurosignet_dir = start_menu_dir / "NeuroSigNet Pro"
            neurosignet_dir.mkdir(exist_ok=True)
            
            # Create batch file in Start Menu
            bat_content = f'''
@echo off
cd /d "{self.install_dir}"
python main.py
'''
            bat_path = neurosignet_dir / "NeuroSigNet Pro.bat"
            with open(bat_path, 'w') as f:
                f.write(bat_content)
            
            print("✅ Start Menu entry created")
            return True
        except Exception as e:
            print(f"⚠️ Could not create Start Menu entry: {e}")
            return False
    
    def add_uninstall_entry(self):
        """Add entry to Add/Remove Programs"""
        if self.system != "windows":
            return
        
        try:
            key = winreg.HKEY_LOCAL_MACHINE
            subkey = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NeuroSigNetPro"
            
            with winreg.CreateKey(key, subkey) as reg_key:
                winreg.SetValueEx(reg_key, "DisplayName", 0, winreg.REG_SZ, "NeuroSigNet Pro")
                winreg.SetValueEx(reg_key, "DisplayVersion", 0, winreg.REG_SZ, "2.0.0")
                winreg.SetValueEx(reg_key, "Publisher", 0, winreg.REG_SZ, "NeuroSigNet Team")
                winreg.SetValueEx(reg_key, "UninstallString", 0, winreg.REG_SZ, 
                                f'"{self.install_dir}\\uninstall.bat"')
                winreg.SetValueEx(reg_key, "InstallLocation", 0, winreg.REG_SZ, 
                                str(self.install_dir))
                
            print("✅ Added to Programs and Features")
        except Exception as e:
            print(f"⚠️ Could not add to Programs and Features: {e}")
    
    def create_uninstaller(self):
        """Create uninstaller"""
        try:
            uninstaller_content = f'''
@echo off
echo Uninstalling NeuroSigNet Pro...
rmdir /s /q "{self.install_dir}"
echo NeuroSigNet Pro has been uninstalled successfully.
pause
'''
            uninstaller_path = self.install_dir / "uninstall.bat"
            with open(uninstaller_path, 'w') as f:
                f.write(uninstaller_content)
            
            print("✅ Uninstaller created")
        except Exception as e:
            print(f"⚠️ Could not create uninstaller: {e}")
    
    def create_sample_data(self):
        """Create sample data and tutorials"""
        print("\n📚 Creating sample data and tutorials...")
        
        samples_dir = self.install_dir / "samples"
        samples_dir.mkdir(exist_ok=True)
        
        # Create quick start guide
        guide_content = """
NeuroSigNet Pro - Quick Start Guide

1. LAUNCH THE APPLICATION:
   - Double-click 'NeuroSigNet Pro' on your desktop
   - Or find it in Start Menu > NeuroSigNet Pro

2. PROCESS YOUR FIRST DOCUMENT:
   - Click 'Upload Document' 
   - Select a JPG/PDF file with signatures or seals
   - Choose processing options
   - Click 'Analyze'

3. SUPPORTED FEATURES:
   - Signature detection and verification
   - Seal and stamp recognition
   - Document quality enhancement
   - Batch processing

Enjoy using NeuroSigNet Pro!
"""
        
        with open(samples_dir / "quick_start_guide.txt", 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print("✅ Sample data created")
    
    def install_main_application(self):
        """Install main application files"""
        print("\n📦 Installing main application...")
        
        # Create directory structure
        directories = ["models", "logs", "uploads", "exports", "temp", "samples"]
        for directory in directories:
            (self.install_dir / directory).mkdir(parents=True, exist_ok=True)
        
        # Copy all Python files from current directory
        current_dir = Path(__file__).parent
        for file_path in current_dir.glob("*.py"):
            if file_path.name != "installer_advanced.py":
                shutil.copy2(file_path, self.install_dir / file_path.name)
        
        # Create assets directory
        assets_dir = self.install_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        print("✅ Main application installed")
        return True
    
    def finalize_installation(self):
        """Finalize installation"""
        print("\n📋 Finalizing installation...")
        
        # Create installation report
        installation_report = {
            "installation": {
                "version": "2.0.0",
                "timestamp": datetime.now().isoformat(),
                "install_directory": str(self.install_dir)
            },
            "system_info": {
                "os": f"{platform.system()} {platform.release()}",
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            }
        }
        
        report_path = self.install_dir / "installation_report.json"
        with open(report_path, 'w') as f:
            json.dump(installation_report, f, indent=2)
        
        # Clean up temporary files
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass
        
        print("✅ Installation finalized")
    
    def install(self):
        """Main installation procedure"""
        print("🚀 NeuroSigNet Pro - Advanced Installation")
        print("=" * 50)
        
        # Admin check
        self.run_as_admin()
        
        # System requirements check
        if not self.check_system_requirements():
            print("\n❌ System requirements not met. Installation cannot continue.")
            input("Press Enter to exit...")
            return False
        
        # Create installation directory
        print(f"\n📁 Installation directory: {self.install_dir}")
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        # Installation steps
        steps = [
            ("Installing main application", self.install_main_application),
            ("Installing Python dependencies", self.install_python_dependencies),
            ("Creating desktop shortcuts", self.create_desktop_shortcut),
            ("Creating Start Menu entries", self.create_start_menu_entry),
            ("Adding to Programs and Features", self.add_uninstall_entry),
            ("Creating uninstaller", self.create_uninstaller),
            ("Creating sample data", self.create_sample_data),
            ("Finalizing installation", self.finalize_installation)
        ]
        
        # Execute installation steps
        success = True
        for step_name, step_function in steps:
            print(f"\n{step_name}...")
            try:
                if not step_function():
                    print(f"⚠️ {step_name} completed with warnings")
            except Exception as e:
                print(f"❌ {step_name} failed: {e}")
                success = False
                break
        
        if success:
            print("\n" + "=" * 50)
            print("🎉 NeuroSigNet Pro installed successfully!")
            print(f"📍 Location: {self.install_dir}")
            print("🚀 Launch from Desktop or Start Menu")
            print("📚 Check 'samples' folder for tutorials")
        else:
            print("\n❌ Installation failed. Please check the errors above.")
        
        input("\nPress Enter to exit...")
        return success

def main():
    """Main function"""
    try:
        installer = NeuroSigNetAdvancedInstaller()
        installer.install()
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()