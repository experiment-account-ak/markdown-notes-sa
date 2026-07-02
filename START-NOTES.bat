@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py manage_notes.py
) else (
  python manage_notes.py
)
pause
