import os, sys, shutil, arcpy
import traceback, time

def log(message):
    arcpy.AddMessage(message)
    with file(sys.argv[0]+".log", 'a') as logFile:
        logFile.write("%s:\t%s\n" % (time.asctime(), message))
    
class Toolbox(object):
    def __init__(self):
        self.label = "WIP tools"
        self.alias = ""
        self.tools = [TopoHydro, ImpCov, Runoff]
        
class TopoHydro(object):
    def __init__(self):
        self.label = "Topography and Hydrology Analysis"
        self.description = "Establishes the watershed and stream network"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Digital Elevation Model",
            name="DEM",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Analysis Mask",
            name="Mask",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        param2 = arcpy.Parameter(
            displayName="Threshold accumulation for Stream formation (acres)",
            name="StreamFormation",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1, param2 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
			# Local variables:
			DEM = "DEM"
			Fill_DEM1 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\Fill_DEM1"
			AnalysisMask = "AnalysisMask"
			Output_drop_raster = ""
			RasterMask01 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\RasterMask01"
			FlowDir_Fill1 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\FlowDir_Fill1"
			FlowAcc_Flow1 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\FlowAcc_Flow1"
			rastercalc = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\rastercalc"
			Reclass_rast1 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\Reclass_rast1"
			StreamT_Reclass1 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\StreamT_Reclass1"

			# Set Geoprocessing environments
			arcpy.env.snapRaster = DEM

			# Process: Fill
		
			arcpy.gp.Fill_sa(DEM, Fill_DEM1, "")
			

			# Process: Flow Direction
			tempEnvironment0 = arcpy.env.cellSize
			arcpy.env.cellSize = "MAXOF"
			tempEnvironment1 = arcpy.env.mask
			arcpy.env.mask = AnalysisMask
			
			arcpy.gp.FlowDirection_sa(Fill_DEM1, FlowDir_Fill1, "NORMAL", Output_drop_raster)
			
			
			arcpy.env.cellSize = tempEnvironment0
			arcpy.env.mask = tempEnvironment1

			# Process: Polygon to Raster
			arcpy.PolygonToRaster_conversion(AnalysisMask, "OBJECTID", RasterMask01, "CELL_CENTER", "NONE", "140")
			

			# Process: Flow Accumulation
			arcpy.gp.FlowAccumulation_sa(FlowDir_Fill1, FlowAcc_Flow1, "", "FLOAT")
			

			# Process: Raster Calculator
			arcpy.gp.RasterCalculator_sa("(\"%FlowAcc_Flow1%\"*1600)/43560", rastercalc)
			

			# Process: Reclassify
			arcpy.gp.Reclassify_sa(rastercalc, "Value", "0 516.96972700000003 NODATA;516.96972700000003 22532.3046875 1", Reclass_rast1, "DATA")
			
			
			# Process: Stream to Feature (2)
			arcpy.gp.StreamToFeature_sa(Reclass_rast1, FlowDir_Fill1, StreamT_Reclass1, "SIMPLIFY")
			


			   #log("Parameters are %s, %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText))
		except Exception as err:
			log(traceback.format_exc())
			log(err)
			raise err
		return

class ImpCov(object):
    def __init__(self):
        self.label = "Imperviousness Analysis"
        self.description = "Impervious area contributions"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Impervious Areas",
            name="ImperviousAreas",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Lakes",
            name="Lakes",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
			# Local variables:
			Reclass_rast1 = "Reclass_rast1"
			FlowDir_Fill1 = "FlowDir_Fill1"
			Impervious = "Impervious"
			Feature_Impe1 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\Feature_Impe1"
			Output_raster__2_ = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\BlockSt_Feat1"
			Output_raster__3_ = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\Aggrega_Bloc1"
			FlowAcc_Flow2 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\FlowAcc_Flow2"
			FlowAcc_Flow1 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\FlowAcc_Flow1"
			rastercalc1 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\rastercalc1"
			Reclass_rast2 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\Reclass_rast2"
			rastercalc2 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\rastercalc2"
			StreamT_rasterc1 = "E:\\GIS_M\\Lab_06\\Lab06\\Lab06Data.gdb\\StreamT_rasterc1"

			# Set Geoprocessing environments
			arcpy.env.snapRaster = "DEM"

			# Process: Feature to Raster
			arcpy.FeatureToRaster_conversion(Impervious, "LENGTH", Feature_Impe1, "4")

			# Process: Block Statistics
			arcpy.gp.BlockStatistics_sa(Feature_Impe1, Output_raster__2_, "Rectangle 10 10 CELL", "SUM", "DATA")

			# Process: Aggregate
			arcpy.gp.Aggregate_sa(Output_raster__2_, Output_raster__3_, "10", "MEAN", "EXPAND", "DATA")

			# Process: Flow Accumulation
			arcpy.gp.FlowAccumulation_sa(FlowDir_Fill1, FlowAcc_Flow2, Output_raster__3_, "FLOAT")

			# Process: Raster Calculator
			arcpy.gp.RasterCalculator_sa("(\"%FlowAcc_Flow2%\"/ \"%FlowAcc_Flow1%\")/100", rastercalc1)

			# Process: Reclassify
			arcpy.gp.Reclassify_sa(rastercalc1, "Value", "0 0.10000000000000001 1;0.10000000000000001 0.20000000000000001 2;0.20000000000000001 0.29999999999999999 3;0.29999999999999999 0.40000000000000002 4;0.40000000000000002 0.5 5;0.5 0.59999999999999998 6;0.59999999999999998 0.69999999999999996 7;0.69999999999999996 0.80000000000000004 8;0.80000000000000004 0.90000000000000002 9;0.90000000000000002 1 10", Reclass_rast2, "DATA")

			# Process: Raster Calculator (2)
			arcpy.gp.RasterCalculator_sa("\"%Reclass_rast1%\" * \"%Reclass_rast2%\"", rastercalc2)

			# Process: Stream to Feature
			arcpy.gp.StreamToFeature_sa(rastercalc2, rastercalc2, StreamT_rasterc1, "SIMPLIFY")

			
			#log("Parameters are %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
        
class Runoff(object):
    def __init__(self):
        self.label = "Runoff Calculations"
        self.description = "Calculation of standard storm flows via USGS regression equations"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Curve Number",
            name="Landuse",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameter is %s" % (parameters[0].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
		
