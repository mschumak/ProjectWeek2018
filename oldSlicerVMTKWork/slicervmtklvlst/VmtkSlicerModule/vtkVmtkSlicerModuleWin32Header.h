/*=auto=========================================================================

  Portions (c) Copyright 2005 Brigham and Women's Hospital (BWH) All Rights Reserved.

  See Doc/copyright/copyright.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Program:   3D Slicer
  Module:    $RCSfile: vtkVmtkSlicerModuleWin32Header.h,v $
  Date:      $Date: 2006/01/06 17:56:51 $
  Version:   $Revision: 1.4 $

=========================================================================auto=*/
// .NAME vtkExampleLoadableGuiLessModuleWin32Header - manage Windows system differences
// .SECTION Description
// The vtkExampleLoadableGuiLessModuleWin32Header captures some system differences between Unix
// and Windows operating systems. 

#ifndef __vtkVmtkSlicerModuleWin32Header_h
#define __vtkVmtkSlicerModuleWin32Header_h

#include <vtkVmtkSlicerModuleConfigure.h>

#if defined(WIN32) && !defined(VTKSLICER_STATIC)
#if defined(VmtkSlicerModule_EXPORTS)
#define VTK_VMTKSLICERMODULE_EXPORT __declspec( dllexport ) 
#else
#define VTK_VMTKSLICERMODULE_EXPORT __declspec( dllimport ) 
#endif
#else
#define VTK_VMTKSLICERMODULE_EXPORT 
#endif

#endif
