@echo off
echo ==================================================
echo Iniciando backend de PMJ localmente (Sin Docker)
echo ==================================================
call venv\Scripts\activate
uvicorn main:app --reload
