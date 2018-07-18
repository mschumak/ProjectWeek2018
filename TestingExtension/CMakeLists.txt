cmake_minimum_required(VERSION 3.5)

project(TestingExtension)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/TestingExtension")
set(EXTENSION_CATEGORY "ProjectWeek2018")
set(EXTENSION_CONTRIBUTORS "Michael Schumaker (Sunnybrook Research Institute), Eman Arnout (London Health Sciences Centre), Olga Trichtchenko (University of Western Ontario)")
set(EXTENSION_DESCRIPTION "An extension to test different VMTK features")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/TestingExtension.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/TestingExtension/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(SurfaceModel)
add_subdirectory(CenterlineFromSurface)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
