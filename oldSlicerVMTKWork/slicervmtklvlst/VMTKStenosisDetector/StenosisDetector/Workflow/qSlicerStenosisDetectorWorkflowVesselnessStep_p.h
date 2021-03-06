/*==============================================================================

  Program: 3D Slicer

  Copyright (c) 2010 Kitware Inc.

  See Doc/copyright/copyright.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Danielle Pace, Kitware Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

#ifndef __qSlicerStenosisDetectorWorkflowVesselnessStep_p
#define __qSlicerStenosisDetectorWorkflowVesselnessStep_p

// Qt includes
#include <QObject>

// CTK includes
#include <ctkPimpl.h>

// Qt includes
#include <QSignalMapper>
class QString;

// EMSegment includes
#include "Workflow/qSlicerStenosisDetectorWorkflowVesselnessStep.h"
//#include "ui_qSlicerStenosisDetectorWelcomeStep.h"
#include "ui_qSlicerStenosisDetectorVesselnessStep.h"

// MRML includes
class vtkMRMLNode;

//-----------------------------------------------------------------------------
class qSlicerStenosisDetectorWorkflowVesselnessStepPrivate : public QObject,
                                              public Ui_qSlicerStenosisDetectorVesselnessStep
{
  Q_OBJECT
  Q_DECLARE_PUBLIC(qSlicerStenosisDetectorWorkflowVesselnessStep)
  int state;
protected:
  qSlicerStenosisDetectorWorkflowVesselnessStep* const q_ptr;
//  bool checked;
public:
  qSlicerStenosisDetectorWorkflowVesselnessStepPrivate(qSlicerStenosisDetectorWorkflowVesselnessStep& object);

  void setupUi(qSlicerStenosisDetectorWorkflowWidgetStep* step);

signals:


protected slots:
//    void advandedHandel();

};

#endif
