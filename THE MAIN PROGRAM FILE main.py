#!/usr/bin/env python3
"""
NeuroSigNet Pro - Professional Document Analysis System
AI-powered signature detection, seal recognition, and document enhancement
"""

import os
import sys
import asyncio
import logging
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

# Добавляем путь к корневой директории
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import socket
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/neurosignet.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NeuroSigNet")

class NeuroSigNetPro:
    """Главный класс приложения NeuroSigNet Pro"""
    
    def __init__(self):
        self.config = self.load_config()
        self.app = FastAPI(
            title="NeuroSigNet Pro",
            description="Professional Document Analysis & AI Enhancement System",
            version="2.0.0",
            docs_url="/api/docs",
            redoc_url="/api/redoc"
        )
        
        self.setup_middleware()
        self.setup_routes()
        self.setup_directories()
        
    def load_config(self):
        """Загрузка конфигурации"""
        return {
            "system": {
                "name": "NeuroSigNet Pro",
                "version": "2.0.0",
                "max_file_size": 100 * 1024 * 1024,
                "allowed_formats": [".jpg", ".jpeg", ".png", ".pdf", ".tiff", ".bmp"]
            },
            "processing": {
                "auto_enhance": True,
                "detect_signatures": True,
                "detect_seals": True
            }
        }
    
    def setup_directories(self):
        """Создание необходимых директорий"""
        directories = ["uploads", "exports", "logs", "temp", "models"]
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
    
    def setup_middleware(self):
        """Настройка middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
    def setup_routes(self):
        """Настройка маршрутов"""
        # Статические файлы
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        self.app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
        self.app.mount("/exports", StaticFiles(directory="exports"), name="exports")
        
        # Основные маршруты
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            return self.get_home_page(request)
            
        @self.app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard(request: Request):
            return self.get_dashboard(request)
            
        @self.app.get("/api/health")
        async def health_check():
            return {
                "status": "healthy",
                "version": "2.0.0",
                "timestamp": datetime.now().isoformat()
            }
            
        @self.app.post("/api/v1/analyze")
        async def analyze_document(
            file: UploadFile = File(...),
            enhance_quality: bool = Form(True),
            detect_signatures: bool = Form(True),
            detect_seals: bool = Form(True),
            language: str = Form("auto")
        ):
            return await self.process_document(file, enhance_quality, detect_signatures, detect_seals, language)
            
        @self.app.post("/api/v1/batch-analyze")
        async def batch_analyze(files: List[UploadFile] = File(...)):
            return await self.process_batch(files)
            
        @self.app.websocket("/ws/progress")
        async def websocket_progress(websocket: WebSocket):
            await self.handle_progress_websocket(websocket)
            
        @self.app.get("/api/v1/history")
        async def get_processing_history(page: int = 1, limit: int = 20):
            return await self.get_history(page, limit)
    
    def get_home_page(self, request: Request):
        """Главная страница"""
        return HTMLResponse("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>NeuroSigNet Pro - Professional Document Analysis</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 0; 
                    padding: 0; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container { 
                    max-width: 800px; 
                    margin: 100px auto; 
                    text-align: center; 
                    padding: 40px;
                }
                .loader {
                    border: 5px solid #f3f3f3;
                    border-top: 5px solid #667eea;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    animation: spin 2s linear infinite;
                    margin: 0 auto 20px;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                h1 { font-size: 2.5em; margin-bottom: 20px; }
                p { font-size: 1.2em; opacity: 0.9; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="loader"></div>
                <h1>NeuroSigNet Pro</h1>
                <p>Loading Professional Document Analysis System...</p>
            </div>
            <script>
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            </script>
        </body>
        </html>
        """)
    
    def get_dashboard(self, request: Request):
        """Панель управления"""
        templates = Jinja2Templates(directory="templates")
        return templates.TemplateResponse("dashboard.html", {"request": request})
    
    async def process_document(self, file: UploadFile, enhance_quality: bool, 
                             detect_signatures: bool, detect_seals: bool, language: str):
        """Обработка документа"""
        try:
            task_id = str(uuid.uuid4())
            file_content = await file.read()
            
            # Сохранение файла
            file_path = f"uploads/{task_id}_{file.filename}"
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            # Имитация обработки (в реальной версии здесь будет AI)
            await asyncio.sleep(2)  # Имитация обработки
            
            result = {
                "task_id": task_id,
                "filename": file.filename,
                "processed": True,
                "signatures_found": 2 if detect_signatures else 0,
                "seals_found": 1 if detect_seals else 0,
                "quality_enhanced": enhance_quality,
                "analysis": {
                    "confidence": 0.95,
                    "processing_time": "2.1s",
                    "document_type": "contract"
                }
            }
            
            return {
                "success": True,
                "task_id": task_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def process_batch(self, files: List[UploadFile]):
        """Пакетная обработка"""
        task_id = str(uuid.uuid4())
        results = []
        
        for file in files:
            result = await self.process_document(
                file=file,
                enhance_quality=True,
                detect_signatures=True,
                detect_seals=True,
                language="auto"
            )
            results.append(result)
        
        return {
            "success": True,
            "task_id": task_id,
            "processed_files": len(results),
            "results": results
        }
    
    async def handle_progress_websocket(self, websocket: WebSocket):
        """WebSocket для отслеживания прогресса"""
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "subscribe_progress":
                    # Имитация прогресса
                    for progress in range(0, 101, 10):
                        await asyncio.sleep(0.5)
                        await websocket.send_text(json.dumps({
                            "type": "progress_update",
                            "task_id": message["task_id"],
                            "progress": progress,
                            "status": "processing"
                        }))
                    
        except WebSocketDisconnect:
            logger.info("WebSocket disconnected")
    
    async def get_history(self, page: int, limit: int):
        """История обработки"""
        return {
            "page": page,
            "limit": limit,
            "total": 0,
            "results": []
        }

# Глобальный экземпляр приложения
neurosignet_app = NeuroSigNetPro()
app = neurosignet_app.app

def find_available_port(start_port=8000, max_attempts=50):
    """Поиск доступного порта"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return start_port

def main():
    """Главная функция запуска"""
    try:
        # Создание необходимых директорий
        os.makedirs("logs", exist_ok=True)
        os.makedirs("uploads", exist_ok=True)
        os.makedirs("exports", exist_ok=True)
        os.makedirs("models", exist_ok=True)
        os.makedirs("temp", exist_ok=True)
        
        # Поиск доступного порта
        port = find_available_port()
        
        print("🚀 Starting NeuroSigNet Pro...")
        print(f"🌐 Web Interface: http://localhost:{port}")
        print(f"📚 API Documentation: http://localhost:{port}/api/docs")
        print("\nPress Ctrl+C to stop the application")
        
        # Запуск сервера
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down NeuroSigNet Pro...")
    except Exception as e:
        print(f"❌ Error starting NeuroSigNet Pro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()