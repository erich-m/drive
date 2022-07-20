import wmi

ANALYSING_TOOL = "AnalysingTool"

w = wmi.WMI()

processes = ANALYSING_TOOL in [f"{p.Name}".replace(".exe","") for p in w.Win32_Process()]
print(processes)