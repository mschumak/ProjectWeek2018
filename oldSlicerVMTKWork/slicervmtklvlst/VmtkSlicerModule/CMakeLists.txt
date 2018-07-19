project(VmtkSlicerModule)

cmake_minimum_required(VERSION 2.4)
if(COMMAND cmake_policy)
  cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

# --------------------------------------------------------------------------
# Find Slicer3

if(NOT Slicer3_SOURCE_DIR)
  find_package(Slicer3 REQUIRED)
  include(${Slicer3_USE_FILE})
  slicer3_set_default_install_prefix_for_external_projects()
endif(NOT Slicer3_SOURCE_DIR)

#-----------------------------------------------------------------------------
# avoid linker bug in Mac OS 10.5
# see:
# http://wiki.finkproject.org/index.php/Fink:Packaging:Preparing_for_10.5#OpenGL_Bug
#
if(APPLE)
  set(CMAKE_SHARED_LINKER_FLAGS "-Wl,-dylib_file,/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib")
  set(CMAKE_EXE_LINKER_FLAGS "-Wl,-dylib_file,/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib")
endif(APPLE)

# --------------------------------------------------------------------------
# Include dirs

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_CURRENT_BINARY_DIR}
  ${Slicer3_Libs_INCLUDE_DIRS}
  ${Slicer3_Base_INCLUDE_DIRS}
  )


configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/vtkVmtkSlicerModuleConfigure.h.in 
  ${CMAKE_CURRENT_BINARY_DIR}/vtkVmtkSlicerModuleConfigure.h
  )

# VMTK SETTINGS
set(VTK_VMTK_CONTRIB OFF) # no user contribs
set(VTK_VMTK_IN_SLICER ON) # activate Slicer install switch

set(TETGEN_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/vtkVmtk/Utilities/tetgen1.4.3) # fix

set(VTK_VMTK_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/vtkVmtk)

set(VTK_VMTK_BUILD_STELLAR OFF) # no need for Stellar

add_subdirectory(
  vmtk/vtkVmtk
)

set(VTK_VMTK_BUILD_STELLAR OFF) # no need for Stellar

# END VMTK SETTINGS

file(GLOB headers "${CMAKE_CURRENT_SOURCE_DIR}/*.h")
install(FILES 
  ${headers} 
  "${CMAKE_CURRENT_BINARY_DIR}/vtkVmtkSlicerModuleConfigure.h"
  DESTINATION ${Slicer3_INSTALL_MODULES_INCLUDE_DIR}/${PROJECT_NAME} COMPONENT Development
  )

# --------------------------------------------------------------------------
# Sources

set(VmtkSlicerModule_SRCS
  vtkVmtkSlicerModuleLogic.cxx
  )

include("${VTK_CMAKE_DIR}/vtkWrapTcl.cmake")
vtk_wrap_tcl3(VmtkSlicerModule 
  VmtkSlicerModule_TCL_SRCS 
  "${VmtkSlicerModule_SRCS}" "")

#---------------------------------------------------------------------------
# Add Loadable Module support

generatelm(VmtkSlicerModule_SRCS 
  VmtkSlicerModule.xml)

# --------------------------------------------------------------------------
# Build and install the library

set(lib_name VmtkSlicerModule)
add_library(${lib_name}
  ${VmtkSlicerModule_SRCS}
  ${VmtkSlicerModule_TCL_SRCS}
  
  )
slicer3_set_modules_output_path(${lib_name})




target_link_libraries(${lib_name}
  ${Slicer3_Libs_LIBRARIES}
  ${Slicer3_Base_LIBRARIES}
  ${KWWidgets_LIBRARIES}
  ${ITK_LIBRARIES}
  vtkvmtkCommonTCL vtkvmtkCommon vtkvmtkComputationalGeometry vtkvmtkComputationalGeometryTCL vtkvmtkDifferentialGeometry vtkvmtkDifferentialGeometryTCL vtkvmtkIO vtkvmtkIOTCL vtkvmtkMisc vtkvmtkMiscTCL vtkvmtkSegmentation vtkvmtkSegmentationTCL vtkvmtkITK vtkvmtkITKTCL
  )


slicer3_install_modules(${lib_name})



