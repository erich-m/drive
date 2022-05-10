import mice
def main():
    DeltaY_World = mice.variables["CONST_PosYm_NorthEastCornerMap"] - mice.variables["CONST_PosYm_SouthWestCornerMap"]
    A = mice.variables["PARAM_ScreenHeight%_ImgMap2D"] / DeltaY_World
    Y = mice.variables["CONST_PosYm_Subject"]
    B = mice.variables["PARAM_ScreenPosY%_ImgMap2D"] - ( mice.variables["PARAM_ScreenHeight%_ImgMap2D"] * mice.variables["CONST_PosYm_SouthWestCornerMap"])/( mice.variables["CONST_PosYm_NorthEastCornerMap"] - mice.variables["CONST_PosYm_SouthWestCornerMap"])
    HalfHeightPlot = mice.variables["PARAM_ScreenHeight%_ImgPlot2D"]/2
    # mice.doDebug("DeltaY_World = "+str(float(DeltaY_World)), 0)
    # mice.doDebug("A = "+str(float(A)), 0)
    # mice.doDebug("Y = "+str(float(Y)), 0)
    # mice.doDebug("B = "+str(float(B)), 0)
    # mice.doDebug("HalfHeightPlot = "+str(float(HalfHeightPlot)), 0)
    # mice.doDebug("AY+B = "+str(float(A*Y + B - HalfHeightPlot )), 0)
    return float(A*Y + B - HalfHeightPlot)