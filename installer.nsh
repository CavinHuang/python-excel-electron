!macro customInstall
  ; 终止应用程序进程
  FindProcDLL::FindProc "Excel自动化处理工具.exe"
  Pop $R0
  StrCmp $R0 "1" 0 noKill
  KillProcDLL::KillProc "Excel自动化处理工具.exe"
noKill:
!macroend