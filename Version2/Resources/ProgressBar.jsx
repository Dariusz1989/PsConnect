/*************************************************************************
* ADOBE CONFIDENTIAL
* ___________________
*
* Copyright 1997-2007 Adobe
* All Rights Reserved.
*
* NOTICE: Adobe permits you to use, modify, and distribute this file in
* accordance with the terms of the Adobe license agreement accompanying
* it. If you have received this file from a source other than Adobe,
* then your use, modification, or distribution of it requires the prior
* written permission of Adobe. 
**************************************************************************/
//========================================================================================
//  
//  $File: //depot/shuksan/source/public/components/xhtmlexport/includes/ProgressBar.jsx $
//  
//  Owner: Roey Horns
//  
//  $Author: martinho $
//  
//  $DateTime: 2006/11/20 16:42:55 $
//  
//  $Revision: 1.1 $
//  
//  $Change: 473185 $
//  
//  
//  
//  Purpose: General purpose progess bar
//  
//  When constructed the progress bar creates a section with a single step.
//  In simple cases you will simply want to call sectionStepFractionCompleted()
//  with a value between 0.0 and 1.0, to signify how far along your script is:
//  
//  var pbar = new ProgressBar('Simple Loop', 'Progress',
//  'To cancel hit the Esc key);
//  for(i = 0; i < numIterations; i++) {
//  doSomeThing();
//  pbar.sectionStepFractionCompleted((i+1)/numIterations);
//  
//  pbar.close();
//  
//  For more complex cases you can define sub-sections that can contain any
//  number of steps, which in turn can be sub-sections.
//  
//  Example: A script first reads in some data from a fileand then writes it to
//  another file. We assume that both operations take roughly he same amount
//  of time. This would look something like:
//  
//  var pbar = new ProgressBar('Copying File', 'Copying File',
//  'To cancel hit the Esc key);
//  pbar.newSection(2);
//  pbar.newSection(numblocks, 'Reading File', 0.5);
//  for(i = 0; i < numblocks; i++) {
//  readblock();
//  pbar.sectionStepCompleted();
//  
//  pbar.sectionCompleted(); // reading
//  pbar.newSection(numblocks, 'Writing File', 0.5);
//  for(i = 0; i < numblocks; i++) {
//  writeblock();
//  pbar.sectionStepCompleted();
//  
//  pbar.sectionCompleted(); // writing
//  pbar.sectionCompleted(); // outermost section
//  pbar.close();
//  
//  This progress bar doesn't have a cancel button since script UI can't process
//  any events other than update events while the script is running. So we rely
//  on InDesign's support for canceling scripts with the Esc key or Cmd-Period.
//  Notice, that the progress bar will not be closed when InDesign cancels the
//  script, so you'll have to find a way to detect the cancelation and close it. 
//  
//========================================================================================


//------------------------------------------------------------------------------
// Constants
//------------------------------------------------------------------------------

//  determines how many milliseconds to wait before opening the progress bar
ProgressBar.openWindowDelay = 100;

// determines how many milliseconds to wait before redrawing the progress bar again
ProgressBar.updateDelay = 0;

//------------------------------------------------------------------------------
// Constructor
//------------------------------------------------------------------------------


function ProgressBar(text, windowtitle, canceltext, fontSize) {
    this.text = text;
    this.windowtitle = windowtitle;
    this.canceltext = canceltext;
    this.isopen = false;
    this.startTime = new Date().getTime();
    this.lastUpdate = 0;
    this.win = null;
    this.sections = new Array();
    this.progress = 0;
    this.fontSize = fontSize
    this.newSection(1, text, 1);
    
} // ProgressBar
    
//------------------------------------------------------------------------------
// ProgressBar.prototype.newSection
// Subdivide the progress bar
// Must be paired with a call to sectionCompleted
// title and fractionOfParentStep are optional arguments
//------------------------------------------------------------------------------

ProgressBar.prototype.newSection = function(numSteps, title, fractionOfParentStep) {
    if (fractionOfParentStep == undefined)
        fractionOfParentStep = 1;
    if (title == undefined)
        title = '';
    var numSections = this.sections.length;
    var start = (numSections > 0 ? this.sections[numSections-1].getTotalFractionComplete() : 0);
    var stepFraction = (numSections > 0 ? this.sections[numSections-1].fractionPerStep : 1);
    var newSection = new ProgressSection(title, start, start + (stepFraction * fractionOfParentStep), numSteps, fractionOfParentStep);
    this.sections.push(newSection);
    if(title != '')
        this.updateText(title);
} // ProgressBar.prototype.newSection


//------------------------------------------------------------------------------
// ProgressBar.prototype.sectionStepFractionCompleted
// Call if you completed a fraction of a step of the current section
//------------------------------------------------------------------------------
        
ProgressBar.prototype.sectionStepFractionCompleted = function(fraction) {
    var numSections = this.sections.length;
    if(numSections > 0) {
        var section = this.sections[numSections - 1];
        section.stepFractionComplete(fraction);
        this.updateProgress(section.getTotalFractionComplete());
    }
} // ProgressBar.prototype.sectionStepFractionCompleted


//------------------------------------------------------------------------------
// ProgressBar.prototype.sectionStepCompleted
// Call if you completed a step of the current section
//------------------------------------------------------------------------------
    
ProgressBar.prototype.sectionStepCompleted = function() {
    var numSections = this.sections.length;
    if(numSections > 0) {
        var section = this.sections[numSections - 1];
        section.stepComplete();
        this.updateProgress(section.getTotalFractionComplete());
    }
} // ProgressBar.prototype.sectionStepCompleted


//------------------------------------------------------------------------------
// ProgressBar.prototype.sectionCompleted
// Call if you completed the current section
//------------------------------------------------------------------------------
    
ProgressBar.prototype.sectionCompleted = function() {
    var section = this.sections.pop();
    var numSections = this.sections.length;
    if(numSections > 0) {
        var parent = this.sections[numSections - 1];
        parent.stepFractionComplete(section.fractionOfParent);
        this.updateProgress(parent.getTotalFractionComplete());
        if(parent.title != '' && section.title != '')
            this.updateText(parent.title);
    }
} // ProgressBar.prototype.sectionCompleted


//------------------------------------------------------------------------------
// ProgressBar.prototype.close
//------------------------------------------------------------------------------
    
ProgressBar.prototype.close = function () {
    if(this.isopen) {
        this.win.close();
        this.isopen = false;
    }
} // ProgressBar.prototype.close
    

//------------------------------------------------------------------------------
// END OF PUBLIC SECTION
//------------------------------------------------------------------------------

//------------------------------------------------------------------------------
// ProgressBar.prototype.open
//------------------------------------------------------------------------------

ProgressBar.prototype.open = function() {
    if(!this.isopen) {
        this.win = new Window( 'palette', this.windowtitle, undefined, { closeButton: false });;
        this.win.main = this.win.add('group',[100,100,480,300]);
        this.win.main.margins = [15,0,15,0];
        this.win.main.orientation = 'column';
        var group = this.win.main.add('group');
        group.orientation = 'column';
        group.alignChildren = ['left', 'fill'];
        this.win.displaytext = group.add('statictext', undefined, this.text,{multiline:true});
        //this.win.displaytext.minimumSize.width = 450
        this.win.displaytext.preferredSize = [350,40];
        if (this.fontSize != null)
        {
            this.win.displaytext.graphics.font = ScriptUI.newFont(this.win.displaytext.graphics.font.name,0,this.fontSize);
        }
        this.win.progressbar = group.add('progressbar', undefined, 0, 1);
        this.win.progressbar.minimumSize.width = 320;
        group.add('statictext', undefined, this.canceltext);
        this.win.layout.layout(true);
        this.win.show();
        this.isopen = true;
    }
} // ProgressBar.prototype.open


//------------------------------------------------------------------------------
// ProgressBar.prototype.updateText
//------------------------------------------------------------------------------
ProgressBar.prototype.updateText = function(text) {
    if(this.isopen) {
        if(this.text != text) {
            this.win.displaytext.text = text;
            this.win.update()
        }
    }
    this.text = text;
} // ProgressBar.prototype.updateText
    

//------------------------------------------------------------------------------
// ProgressBar.prototype.updateProgress
//------------------------------------------------------------------------------
ProgressBar.prototype.updateProgress = function(progressValue) {
    var now = new Date().getTime();
    if(!this.isopen) {
        if(now - this.startTime >= ProgressBar.openWindowDelay) {
            this.progress = progressValue;
            this.open();
        }
    } else {
        if(progressValue > this.progress) {
            this.progress = progressValue;
            if (now - this.lastUpdate >= ProgressBar.updateDelay) {
                this.lastUpdate = now;
                this.win.progressbar.value = progressValue;
            }
        }
    }   
} // ProgressBar.prototype.updateProgress


//------------------------------------------------------------------------------
// Definition and Implementation for ProgressSection Object
//------------------------------------------------------------------------------

//------------------------------------------------------------------------------
// Constructor
//------------------------------------------------------------------------------
    
function ProgressSection(title, start, end, numSteps, fractionOfParentStep) {
    this.start = start;
    this.end = end;
    this.numSteps = numSteps;
    this.fractionPerStep = (end-start)/numSteps;
    this.stepsComplete = 0;
    this.curStepFractionComplete = 0;
    this.fractionOfParent = fractionOfParentStep;
    this.title = title;
} // ProgressSection


//------------------------------------------------------------------------------
// ProgressSection.prototype.stepComplete
//------------------------------------------------------------------------------

ProgressSection.prototype.stepComplete = function() {
    this.stepsComplete++;
    this.curStepFractionComplete = 0;
} // ProgressSection.prototype.stepComplete


//------------------------------------------------------------------------------
// CProgressSection.prototype.stepFractionComplete
// This allows to mark a fraction of the current section as being complete
//------------------------------------------------------------------------------

ProgressSection.prototype.stepFractionComplete = function(fraction) {
    this.curStepFractionComplete = fraction;
} // ProgressSection.prototype.stepFractionComplete


//------------------------------------------------------------------------------
// ProgressSection.prototype.getTotalFractionComplete
//------------------------------------------------------------------------------

ProgressSection.prototype.getTotalFractionComplete = function() {
    return this.start + (this.stepsComplete * this.fractionPerStep) + (this.curStepFractionComplete * this.fractionPerStep);
} // ProgressSection.prototype.getTotalFractionComplete