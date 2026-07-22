@echo off
rem Rebuilds the Windows agent and drops it into the locally installed service,
rem for fast iteration without reinstalling the MSI.

set service_name=CheckMkService
set service_dir=%ProgramFiles(x86)%\checkmk\service
set built_exe=build\check_mk_service\x64\Release\check_mk_service.exe

call pwsh -File run.ps1 -W

net stop %service_name%
copy /Y %built_exe% "%service_dir%\check_mk_service.exe"
copy /Y %built_exe% "%service_dir%\check_mk_agent.exe"
net start %service_name%
