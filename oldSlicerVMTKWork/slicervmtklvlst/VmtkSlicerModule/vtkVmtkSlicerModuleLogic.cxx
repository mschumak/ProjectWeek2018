/*=auto=========================================================================

Portions (c) Copyright 2005 Brigham and Women's Hospital (BWH) All Rights Reserved.

See Doc/copyright/copyright.txt
or http://www.slicer.org/copyright/copyright.txt for details.

Program:   3D Slicer
Module:    $RCSfile: vtkVmtkSlicerModuleLogic.cxx,v $
Date:      $Date: 2006/03/17 15:10:10 $
Version:   $Revision: 1.2 $

=========================================================================auto=*/

#include <string>
#include <iostream>
#include <sstream>

#include "vtkObjectFactory.h"

#include "vtkVmtkSlicerModuleLogic.h"
#include "vtkVmtkSlicerModule.h"
#include "vtkSlicerApplication.h"
#include "vtkTcl.h" // Needed for Tcl_Interp


extern "C" int Vtkvmtkcommontcl_Init(Tcl_Interp *interp);
extern "C" int Vtkvmtkcomputationalgeometrytcl_Init(Tcl_Interp *interp);
extern "C" int Vtkvmtkdifferentialgeometrytcl_Init(Tcl_Interp *interp);
extern "C" int Vtkvmtkiotcl_Init(Tcl_Interp *interp);
extern "C" int Vtkvmtkmisctcl_Init(Tcl_Interp *interp);
extern "C" int Vtkvmtksegmentationtcl_Init(Tcl_Interp *interp);
extern "C" int Vtkvmtkitktcl_Init(Tcl_Interp *interp);

vtkVmtkSlicerModuleLogic* vtkVmtkSlicerModuleLogic::New()
{
  // First try to create the object from the vtkObjectFactory
  vtkObject* ret = vtkObjectFactory::CreateInstance("vtkVmtkSlicerModuleLogic");
  if(ret)
    {
      return (vtkVmtkSlicerModuleLogic*)ret;
    }



  // If the factory was unable to create the object, then create it here.
  return new vtkVmtkSlicerModuleLogic;
}


//----------------------------------------------------------------------------
vtkVmtkSlicerModuleLogic::vtkVmtkSlicerModuleLogic()
{

  Tcl_Interp *interp = NULL;
  vtkSlicerApplication *slicerApp = vtkSlicerApplication::GetInstance ( );
  interp = slicerApp->GetMainInterp();
  if (!interp)
    {
      std::cout << "Error: InitializeTcl failed" << std::endl;
    
    } else {


      Vtkvmtkcommontcl_Init(interp);
      Vtkvmtkcomputationalgeometrytcl_Init(interp);
      Vtkvmtkdifferentialgeometrytcl_Init(interp);
      Vtkvmtkiotcl_Init(interp);
      Vtkvmtkmisctcl_Init(interp);
      Vtkvmtksegmentationtcl_Init(interp);
      Vtkvmtkitktcl_Init(interp);

    }

}

//----------------------------------------------------------------------------
vtkVmtkSlicerModuleLogic::~vtkVmtkSlicerModuleLogic()
{

}

//----------------------------------------------------------------------------
void vtkVmtkSlicerModuleLogic::PrintSelf(ostream& os, vtkIndent indent)
{
  
}

void vtkVmtkSlicerModuleLogic::Apply()
{

}
