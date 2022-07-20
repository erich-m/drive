import wmi

ANALYSING_TOOL = "AnalysingTool"

# w = wmi.WMI()
# processes = ANALYSING_TOOL in [f"{p.Name}".replace(".exe","") for p in w.Win32_Process()]#check if the Analysis tool is running or not
# print(processes)


# C:\OKTAL\SCANeRstudio_1.6\bin\x64\AnalysingTool.exe -c DRIVER_DS_1.6 C:/OKTAL/SCANeRstudio_1.6/data/GUELPH_DATA_1.6/record/MTO_MWPractice - Copy-31_01_2018-17h54m37s/MTO_MWPractice - Copy-31_01_2018-17h54m37s.recprj

#AnalysingTool.exe -c DRIVER_DS_1.6 "C:/OKTAL/SCANeRstudio_1.6/data/GUELPH_DATA_1.6/record/MTO_MWPractice - Copy-31_01_2018-17h54m37s/MTO_MWPractice - Copy-31_01_2018-17h54m37s.recprj"