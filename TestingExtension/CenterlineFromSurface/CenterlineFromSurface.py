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


        #Do stuff!


    #end GenerateCenterlineFromSurface



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


