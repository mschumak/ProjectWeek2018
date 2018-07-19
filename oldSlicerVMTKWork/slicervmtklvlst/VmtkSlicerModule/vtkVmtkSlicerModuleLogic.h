/*=auto=========================================================================

  Portions (c) Copyright 2008 Brigham and Women's Hospital (BWH) All Rights Reserved.

  See Doc/copyright/copyright.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Program:   3D Slicer
  Module:    $RCSfile: vtkExampleLoadableGuiLessModuleLogic.h,v $
  Date:      $Date: 2006/03/19 17:12:29 $
  Version:   $Revision: 1.3 $

=========================================================================auto=*/
#ifndef __vtkVmtkSlicerModuleLogic_h
#define __vtkVmtkSlicerModuleLogic_h

#include "vtkSlicerModuleLogic.h"

#include "vtkVmtkSlicerModule.h"



class vtkITKGradientAnisotropicDiffusionImageFilter;

class VTK_VMTKSLICERMODULE_EXPORT vtkVmtkSlicerModuleLogic : public vtkSlicerModuleLogic
{
  public:
  static vtkVmtkSlicerModuleLogic *New();
  vtkTypeMacro(vtkVmtkSlicerModuleLogic,vtkSlicerModuleLogic);
  void PrintSelf(ostream& os, vtkIndent indent);

  // TODO: do we need to observe MRML here?
  virtual void ProcessMrmlEvents ( vtkObject *caller, unsigned long event,
                                   void *callData ){};


  // The method that creates and runs VTK or ITK pipeline
  void Apply();
  
protected:
  vtkVmtkSlicerModuleLogic();
  virtual ~vtkVmtkSlicerModuleLogic();
  vtkVmtkSlicerModuleLogic(const vtkVmtkSlicerModuleLogic&);
  void operator=(const vtkVmtkSlicerModuleLogic&);

};

#endif

