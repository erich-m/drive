import mice
def main():
    DeltaX_World = mice.variables["CONST_PosXm_NorthEastCornerMap"] - mice.variables["CONST_PosXm_SouthWestCornerMap"]
    A = mice.variables["PARAM_ScreenWidth%_ImgMap2D"] / DeltaX_World
    X = mice.variables["CONST_PosXm_Subject"]
    B = mice.variables["PARAM_ScreenPosX%_ImgMap2D"] - ( mice.variables["PARAM_ScreenWidth%_ImgMap2D"] * mice.variables["CONST_PosXm_SouthWestCornerMap"])/( mice.variables["CONST_PosXm_NorthEastCornerMap"] - mice.variables["CONST_PosXm_SouthWestCornerMap"])
    HalfWidthPlot = mice.variables["PARAM_ScreenWidth%_ImgPlot2D"]/2
    # mice.doDebug("DeltaX_World = "+str(float(DeltaX_World)), 0)
    # mice.doDebug("A = "+str(float(A)), 0)
    # mice.doDebug("X = "+str(float(X)), 0)
    # mice.doDebug("B = "+str(float(B)), 0)
    # mice.doDebug("HalfWidthPlot = "+str(float(HalfWidthPlot)), 0)
    # mice.doDebug("AX+B = "+str(float(A*X + B - HalfWidthPlot )), 0)
    return float(A*X + B - HalfWidthPlot)