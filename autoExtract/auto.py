import os
import signal

import wmi

ANALYSING_TOOL = "AnalysingTool"

w = wmi.WMI()
appNames = [f"{p.Name}".replace(".exe","") for p in w.Win32_Process()]#check if the Analysis tool is running or not
appPids = [f"{p.ProcessId}" for p in w.Win32_Process()]#check if the Analysis tool is running or not

apps = dict(zip(appNames,appPids))



print(apps)

# C:\OKTAL\SCANeRstudio_1.6\bin\x64\AnalysingTool.exe -c DRIVER_DS_1.6 C:/OKTAL/SCANeRstudio_1.6/data/GUELPH_DATA_1.6/record/MTO_MWPractice - Copy-31_01_2018-17h54m37s/MTO_MWPractice - Copy-31_01_2018-17h54m37s.recprj

#AnalysingTool.exe -c DRIVER_DS_1.6 "C:/OKTAL/SCANeRstudio_1.6/data/GUELPH_DATA_1.6/record/MTO_MWPractice - Copy-31_01_2018-17h54m37s/MTO_MWPractice - Copy-31_01_2018-17h54m37s.recprj"

# C:\OKTAL\SCANeRstudio_1.6\bin\x64\AnalysingTool.exe -c GUELPH_DATA_1.6 C:/OKTAL/SCANeRstudio_1.6/data/DEFAULT/record/test-07_08_2022-16h33m55s/test-07_08_2022-16h33m55s.recprj
