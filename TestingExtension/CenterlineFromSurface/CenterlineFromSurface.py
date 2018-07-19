import os
import unittest
import vtk, qt, ctk, slicer, numpy, math
from slicer.ScriptedLoadableModule import *
import vtkSegmentationCorePython as vtkSegmentationCore
import logging

#
# CenterlineFromSurface
class CenterlineFromSurface(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "CenterlineFromSurface" # TODO make this more human readable by adding spaces
    self.parent.categories = ["ProjectWeek2018"]
    self.parent.dependencies = []
    self.parent.contributors = ["Michael Schumaker (Sunnybrook Research Institute), Eman Arnout (London Health Sciences Centre), Olga Trichtchenko (University of Western Ontario)"] 
    self.parent.helpText = """Starting with a vascular model defined as a surface, a single source and a single target, obtain one centerline."""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """Michael Schumaker (Sunnybrook Research Institute), Eman Arnout (London Health Sciences Centre), Olga Trichtchenko (University of Western Ontario)"""

#
# CenterlineFromSurfaceWidget
class CenterlineFromSurfaceWidget(ScriptedLoadableModuleWidget):
    """The module's appearance"""

    def __init__(self, parent):
        """Constructor for CenterlineFromSurfaceWidget, creates the self.logic object and other members."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        self.theLayoutManager = slicer.app.layoutManager()
        self.logic = CenterlineFromSurfaceLogic()
        self.moduleDir = os.path.dirname(slicer.util.modulePath(self.__module__))
    #end __init__
    
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        self.layout.addStretch(1)

        #surfaceModel model selector
        self.surfaceModelSelector = slicer.qMRMLNodeComboBox()
        self.surfaceModelSelector.nodeTypes = ["vtkMRMLModelNode"]
        self.surfaceModelSelector.selectNodeUponCreation = True
        self.surfaceModelSelector.addEnabled = False
        self.surfaceModelSelector.removeEnabled = False
        self.surfaceModelSelector.noneEnabled = False
        self.surfaceModelSelector.showHidden = False
        self.surfaceModelSelector.showChildNodeTypes = True
        self.surfaceModelSelector.setMRMLScene( slicer.mrmlScene)
        self.surfaceModelSelector.setToolTip("Load a ")
        self.layout.addWidget(self.addRow("Surface Model: ", self.surfaceModelSelector))
        
        #Centerline model selector (temporarily)
        self.centerlineSelector = slicer.qMRMLNodeComboBox()
        self.centerlineSelector.nodeTypes = ["vtkMRMLModelNode"]
        self.centerlineSelector.selectNodeUponCreation = True
        self.centerlineSelector.addEnabled = True
        self.centerlineSelector.removeEnabled = True
        self.centerlineSelector.noneEnabled = True
        self.centerlineSelector.showHidden = False
        self.centerlineSelector.showChildNodeTypes = False
        self.centerlineSelector.setMRMLScene( slicer.mrmlScene)
        self.centerlineSelector.setToolTip("Set a model node for the output centerline")
        self.layout.addWidget(self.addRow("Centerline Output: ", self.centerlineSelector))

        self.layout.addWidget(qt.QLabel("Some way to set the source and target points will be needed"))
        self.layout.addWidget(qt.QLabel(" "))

        #A button to perform the desired action
        self.applyButton = qt.QPushButton("Run")
        self.applyButton.enabled = False
        self.layout.addWidget(self.addRow("Run: ", self.applyButton))

        self.layout.addStretch(1)

        #Connections
        self.applyButton.connect('clicked(bool)', self.onApplyButton)
        self.surfaceModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.centerlineSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    #end setup
        
        
    def onSelect(self):
        """What to do when one of the nodes in the selector is changed."""
        self.applyButton.enabled = self.surfaceModelSelector.currentNode() and self.centerlineSelector.currentNode()


    def onApplyButton(self):
        """What action should be taken when the button is clicked?"""
        if(self.surfaceModelSelector.currentNode() and self.centerlineSelector.currentNode()):
            #Still need to do something about the start and end points
            self.logic.GenerateCenterlineFromSurface(self.surfaceModelSelector.currentNode(), self.centerlineSelector.currentNode())
    #end onApplyButton

        
    def addRow(self, pretext, newWidget):
        rowWidget = qt.QWidget()
        rowLayout = qt.QFormLayout()
        rowWidget.setLayout(rowLayout)
        try:
            rowLayout.addRow(pretext, newWidget)
        except AttributeError:
            pass
        finally:
            return rowWidget
    #end addRow

    def cleanup(self):
        pass

#end CenterlineFromSurfaceWidget


#
# CenterlineFromSurfaceLogic
class CenterlineFromSurfaceLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual computation done by your module.  The interface should be such that other python code can import this class and make use of the functionality without requiring an instance of the Widget. Uses ScriptedLoadableModuleLogic base class, available at: https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py """


    def GenerateCenterlineFromSurface(self, surfaceModelNode, centerlineNode):
        """Do something to generate a centerline."""
        print "GenerateCenterlineFromSurface has been called!"
        #Try using VMTK Python classes directly. Do not use SlicerExtension-VMTK methods

        #Type is vtkMRMLModelNode
        try:
            surfaceModelPolyData = surfaceModelNode.GetPolyData()
        except (NameError, AttributeError):
            print "Could not extract vtkPolyData from model node in GenerateCenterlineFromSurface"
            return None

        #Get the IDs of a source and a target point already in the model
        sourceAndTargetListReturn = self.GetSingleSourceAndTargetPointsList(surfaceModelNode.GetID())
        if(sourceAndTargetListReturn is None):
           print "Could not extract source and target points from model node in GenerateCenterlineFromSurface"
           return None
        sourcePointList = sourceAndTargetListReturn[0]
        targetPointList = sourceAndTargetListReturn[1]
        print "sourcePointList={}, targetPointList={}".format(sourcePointList, targetPointList)
        
        #Attempt 1: do it the simple and inaccurate way by generating a network model
        centerlinePolyData = self.GenerateNetwork(surfaceModelPolyData, sourcePointList)
        if(centerlinePolyData is not None):
            centerlineNode.SetAndObservePolyData(centerlinePolyData)
        else:
            print "Could not generate centerline in GenerateCenterlineFromSurface"
            return

    #end GenerateCenterlineFromSurface


    def GenerateNetwork(self, surfaceModelNode, sourcePointList):
        """Create a centerline the simple and inaccurate way - start at a single point, and let the network calculation find one or more end points."""
        print "Entered GenerateNetwork"

        # import the vmtk libraries
        try:
            import vtkvmtkComputationalGeometryPython as vtkvmtkComputationalGeometry
            import vtkvmtkMiscPython as vtkvmtkMisc
        except ImportError:
            print "Unable to import the SlicerVmtk libraries"
            return None

        radiusArrayName = 'Radius'
        topologyArrayName = 'Topology'
        marksArrayName = 'Marks'

        networkExtraction = vtkvmtkMisc.vtkvmtkPolyDataNetworkExtraction()
        networkExtraction.SetInputData(polyData)
        networkExtraction.SetAdvancementRatio(1.05)
        networkExtraction.SetRadiusArrayName(radiusArrayName)
        networkExtraction.SetTopologyArrayName(topologyArrayName)
        networkExtraction.SetMarksArrayName(marksArrayName)
        networkExtraction.Update()

        outPolyData = vtk.vtkPolyData()
        outPolyData.DeepCopy(networkExtraction.GetOutput())

        return outPolyData
    #end GenerateNetwork


    def GetSingleSourceAndTargetPoints(self, modelNodeID):
        """Use the method GetSingleSourceAndTargetPointsList to obtain the IDs of source and target points. Get the 3-element positions of those points, and return a 2-tuple containing the 3-element points. This method does not identify multiple target points. Returns None on error."""
        #Type is vtkMRMLModelNode
        try:
            modelNode = slicer.util.getNode(modelNodeID)
            modelPolyData = modelNode.GetPolyData()
        except (NameError, AttributeError):
            print "Could not extract vtkPolyData from model node in GetSingleSourceAndTargetPoints"
            return None
        #Call the method that actually finds the source and target points,
        #and returns a list of the point IDs
        listReturn = self.GetSingleSourceAndTargetPointsList(modelNodeID)
        if(listReturn is None):
           print "Could not extract source and target points from model node in GetSingleSourceAndTargetPoints"
           return None
        sourceIdList = listReturn[0]
        targetIdList = listReturn[1]
        try:
            if((sourceIdList.GetNumberOfIds() == 0) or (targetIdList.GetNumberOfIds() == 0)):
                raise ValueError("Could not extract source and target points from model node in GetSingleSourceAndTargetPoints")
        except (AttributeError, IndexError, ValueError):
            print "Could not extract source and target points from model node in GetSingleSourceAndTargetPoints"
            return None
        sourcePoint = [0,0,0]
        targetPoint = [0,0,0]
        modelPolyData.GetPoint(sourceIdList.GetId(0), sourcePoint)
        modelPolyData.GetPoint(targetIdList.GetId(0), targetPoint)
        return (sourcePoint, targetPoint)
    #end GetSingleSourceAndTargetPoints

    def GetSingleSourceAndTargetPointsList(self, modelNodeID):
        """Start by getting the RAS bounds of the model. Get points at the min and max axial values. Find a point with the same axial value for each (min and max). This version of the method does not identify multiple target points. Returns None on error."""
        #Type is vtkMRMLModelNode
        try:
            modelNode = slicer.util.getNode(modelNodeID)
            modelPolyData = modelNode.GetPolyData()
        except (NameError, AttributeError):
            print "Could not extract vtkPolyData from model node in GetSingleSourceAndTargetPointsList"
            return None
        #Get the axial bounds of the model
        RASBounds = [0,0,0,0,0,0]
        modelNode.GetRASBounds(RASBounds)
        minAxial = RASBounds[4]
        maxAxial = RASBounds[5]

        #Get the Ids of points that have axial values at the bounds
        sourcePointFound = False
        sourcePointId = -1
        targetPointFound = False
        targetPointId = -1
        numPoints = modelPolyData.GetNumberOfPoints()
        for ptId in range(numPoints):
            pointPos = [0,0,0]
            modelPolyData.GetPoint(ptId, pointPos)
            if((pointPos[2] == maxAxial) and not sourcePointFound):
                sourcePointFound = True
                sourcePointId = ptId
            elif((pointPos[2] == minAxial) and not targetPointFound):
                targetPointFound = True
                targetPointId = ptId
            if(sourcePointFound and targetPointFound):
                break
        if((sourcePointId == -1) or (targetPointId == -1)):
            print "Could not find source or target point in GetSingleSourceAndTargetPointsList"
            return None

        #Assign the point ids to vtkIdLists
        sourceIdList = vtk.vtkIdList()
        targetIdList = vtk.vtkIdList()
        sourceIdList.InsertUniqueId(sourcePointId)
        targetIdList.InsertUniqueId(targetPointId)
        return (sourceIdList, targetIdList)
    #end GetSingleSourceAndTargetPointsList



#end CenterlineFromSurfaceLogic


class CenterlineFromSurfaceTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """
    
    def setUp(self):
        """ Do a scene clear to reset the state.
        """
        #slicer.mrmlScene.Clear(0)
        #Don't clear when Test is clicked. Not right now.
        pass
    
    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_CenterlineFromSurface1()
    
    def test_CenterlineFromSurface1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """
        
        self.delayDisplay("Starting the test")
        
        #for url,name,loader in downloads:
        #  filePath = slicer.app.temporaryPath + '/' + name
        #  if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        #    logging.info('Requesting download %s from %s...\n' % (name, url))
        
        #volumeNode = slicer.util.getNode(pattern="FA")
        #logic = FusionWorkflowLogic()
        
        self.delayDisplay('Test passed!')
    #end test_CenterlineFromSurface1

#end class CenterlineFromSurfaceTest


