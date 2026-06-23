@echo off
chcp 65001 >nul
echo ===============================================
echo    Iniciando Alineamiento Multilingüe de Poesía
echo ===============================================

REM Verificar si Python está instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no está instalado en este ordenador.
    echo Por favor, descarga e instala Python gratuitamente desde la Microsoft Store.
    echo O desde la web oficial: https://www.python.org/downloads/
    echo ¡IMPORTANTE!: Durante la instalacion, recuerda marcar la casilla "Add python.exe to PATH".
    pause
    exit /b
)

REM Crear entorno virtual si no existe
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo Configurando la herramienta por primera vez ^(esto tomará unos minutos^)...
    python -m venv venv
)

REM Activar el entorno virtual
call venv\Scripts\activate.bat

echo Verificando dependencias...
pip install -r requirements.txt >nul 2>&1

echo ¡Todo listo! Abriendo la aplicacion en tu navegador...
streamlit run app.py

pause
