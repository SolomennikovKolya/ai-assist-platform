# AI-Assist Platform BackEnd

Это репозиторий с кодом для бэкэнда платформы по созданию ИИ-ассистентов.

# Installation

Ниже представлены инструкции по установке проекта для windows:
```
git clone http://gitlab.sberlab.nsu.ru/n.solomennikov/ai-assist-platform-backend.git
cd ai-assist-platform-backend
python -m venv local_venv
.\local_venv\Scripts\activate.bat
pip install -r requirements.txt
cp .env_example .env
```
В файле .env замените [OPENAI_API_KEY] на свой ключ от openai.
Также замените base_url на адрес прокси сервера для работы с openai, так как base_url по умолчанию может не работать.

# Usage

python src\main.py
