   def TrimCenterline(self, inputData, inBounds):
        """Given a vtkPolyData (inputData) and axial bounds specifying the desired range, this method cuts the model to the specified axial bounds. This method receives and returns vtkPolyData objects (contrary to standard VTK pipeline format). On error, it returns None."""
        #Check the type of input
        try:
            if(not inputData.IsA("vtkPolyData")):
                raise TypeError("inputData is not the right type in CenterlinesModuleLogic.TrimCenterline")
        except (NameError, AttributeError, TypeError):
           print "inputData cannot be accessed or is not the right type in CenterlinesModuleLogic.TrimCenterline"
           return None

        #Get the bounds of inputData
        inputDataBounds = [0,0,0,0,0,0]
        inputData.GetBounds(inputDataBounds)

        #Create a vtkBox, which is a subclass of vtkImplicitFunction.
        #Use the inputData bounds from the first two axes, and constrain it
        #to the range in the parameter 'inBounds' in the third axis
        cube = vtk.vtkBox()
        xMin = inputDataBounds[0]
        xMax = inputDataBounds[1]
        yMin = inputDataBounds[2]
        yMax = inputDataBounds[3]
        zMin = inBounds[0]
        zMax = inBounds[1]
        cube.SetBounds(xMin,xMax,yMin,yMax,zMin,zMax)

        clip = vtk.vtkClipPolyData()
        clip.GenerateClippedOutputOff()
        clip.InsideOutOn() #Select what's IN the box
        clip.SetClipFunction(cube)
        clip.SetInputData(inputData)
        clip.Update()
        return clip.GetOutput()
    #end TrimCenterline
