
// $(document).ready(function() {
// var pageRefresh = 7000; // 7s
//     setInterval(function() {
//         refresh();
//     }, pageRefresh);
// });

// Functions

function refresh() {
    //$('#DivBrowserRefresh').load(location.href + " #DivBrowserRefresh");
    //$('#DivBrowserRefresh').load();
    $("#DivBrowserRefresh").load(location.href+" #myDiv *","");
    $("#DivBrowserRefresh").load(location.href+" #DivBrowserRefresh>*","");
}


$(document).ready(function(){
  // Set div display to Brave
  $(".show-brave").click(function(){
    $("#myDivbrave").css("display", "block");
    $("#myDivfire").css("display", "none");
    $("#myDivchrome").css("display", "none");
    $("#myDivchromium").css("display", "none");
    $("#myDivvivaldi").css("display", "none");
    $("#myDivopera").css("display", "none");
    $("#myDivlibrewolf").css("display", "none");
    $("#myDivfalkon").css("display", "none");
    $("#myDivedge").css("display", "none");
    refresh();
  });
  
  // Set div display to Firefox
  $(".show-fire").click(function(){
    $("#myDivbrave").css("display", "none");
    $("#myDivfire").css("display", "block");
    $("#myDivchrome").css("display", "none");
    $("#myDivchromium").css("display", "none");
    $("#myDivvivaldi").css("display", "none");
    $("#myDivopera").css("display", "none");
    $("#myDivlibrewolf").css("display", "none");
    $("#myDivfalkon").css("display", "none");
    $("#myDivedge").css("display", "none");
    refresh();
  });
  // Set div display Google Chrome
  $(".show-chrome").click(function(){
    $("#myDivbrave").css("display", "none");
    $("#myDivfire").css("display", "none");
    $("#myDivchrome").css("display", "block");
    $("#myDivchromium").css("display", "none");
    $("#myDivvivaldi").css("display", "none");
    $("#myDivopera").css("display", "none");
    $("#myDivlibrewolf").css("display", "none");
    $("#myDivfalkon").css("display", "none");
    $("#myDivedge").css("display", "none");
    refresh();
  });
  // Set div display Chromium
  $(".show-chromium").click(function(){
    $("#myDivbrave").css("display", "none");
    $("#myDivfire").css("display", "none");
    $("#myDivchrome").css("display", "none");
    $("#myDivchromium").css("display", "block");
    $("#myDivvivaldi").css("display", "none");
    $("#myDivopera").css("display", "none");
    $("#myDivlibrewolf").css("display", "none");
    $("#myDivfalkon").css("display", "none");
    $("#myDivedge").css("display", "none");
    refresh();
  });
  // Set div display Vivaldi
  $(".show-vivaldi").click(function(){
    $("#myDivbrave").css("display", "none");
    $("#myDivfire").css("display", "none");
    $("#myDivchrome").css("display", "none");
    $("#myDivchromium").css("display", "none");
    $("#myDivvivaldi").css("display", "block");
    $("#myDivopera").css("display", "none");
    $("#myDivlibrewolf").css("display", "none");
    $("#myDivfalkon").css("display", "none");
    $("#myDivedge").css("display", "none");
    refresh();
  });
  // Set div display Opera
  $(".show-opera").click(function(){
    $("#myDivbrave").css("display", "none");
    $("#myDivfire").css("display", "none");
    $("#myDivchrome").css("display", "none");
    $("#myDivchromium").css("display", "none");
    $("#myDivvivaldi").css("display", "none");
    $("#myDivopera").css("display", "block");
    $("#myDivlibrewolf").css("display", "none");
    $("#myDivfalkon").css("display", "none");
    $("#myDivedge").css("display", "none");
    refresh();
  });
  // Set div display librewolf
  $(".show-librewolf").click(function(){
    $("#myDivbrave").css("display", "none");
    $("#myDivfire").css("display", "none");
    $("#myDivchrome").css("display", "none");
    $("#myDivchromium").css("display", "none");
    $("#myDivvivaldi").css("display", "none");
    $("#myDivopera").css("display", "none");
    $("#myDivlibrewolf").css("display", "block");
    $("#myDivfalkon").css("display", "none");
    $("#myDivedge").css("display", "none");
    refresh();
  });
  // Set div display falkon
  $(".show-falkon").click(function(){
    $("#myDivbrave").css("display", "none");
    $("#myDivfire").css("display", "none");
    $("#myDivchrome").css("display", "none");
    $("#myDivchromium").css("display", "none");
    $("#myDivvivaldi").css("display", "none");
    $("#myDivopera").css("display", "none");
    $("#myDivlibrewolf").css("display", "none");
    $("#myDivfalkon").css("display", "block");
    $("#myDivedge").css("display", "none");
    refresh();
  // Set div display edge
  $(".show-edge").click(function(){
    $("#myDivbrave").css("display", "none");
    $("#myDivfire").css("display", "none");
    $("#myDivchrome").css("display", "none");
    $("#myDivchromium").css("display", "none");
    $("#myDivvivaldi").css("display", "none");
    $("#myDivopera").css("display", "none");
    $("#myDivlibrewolf").css("display", "none");
    $("#myDivfalkon").css("display", "none");
    $("#myDivedge").css("display", "block");
    refresh();
  });
});

class Steps {
  constructor(wizard) {
    this.wizard = wizard;
    this.steps = this.getSteps();
    this.stepsQuantity = this.getStepsQuantity();
    this.currentStep = 0;
  }

  setCurrentStep(currentStep) {
    this.currentStep = currentStep;
  }

  getSteps() {
    return this.wizard.getElementsByClassName('step');
  }

  getStepsQuantity() {
    return this.getSteps().length;
  }

  handleConcludeStep() {
    this.steps[this.currentStep].classList.add('-completed');
  }

  handleStepsClasses(movement) {
    if (movement > 0)
    this.steps[this.currentStep - 1].classList.add('-completed');else
    if (movement < 0)
    this.steps[this.currentStep].classList.remove('-completed');
  }}


class Panels {
  constructor(wizard) {
    this.wizard = wizard;
    this.panelWidth = this.wizard.offsetWidth;
    this.panelsContainer = this.getPanelsContainer();
    this.panels = this.getPanels();
    this.currentStep = 0;

    this.updatePanelsPosition(this.currentStep);
    this.updatePanelsContainerHeight();
  }

  getCurrentPanelHeight() {
    return `${this.getPanels()[this.currentStep].offsetHeight}px`;
  }

  getPanelsContainer() {
    return this.wizard.querySelector('.panels');
  }

  getPanels() {
    return this.wizard.getElementsByClassName('panel');
  }

  updatePanelsContainerHeight() {
//     this.panelsContainer.style.height = this.getCurrentPanelHeight();
  }

  updatePanelsPosition(currentStep) {
    const panels = this.panels; //CONTA QUANTOS PAINEIS
    const panelWidth = this.panelWidth;

    for (let i = 0; i < panels.length; i++) {//FOR DOS PAINEIS
      panels[i].classList.remove(
      'movingIn',
      'movingOutBackward',
      'movingOutFoward');


      if (i !== currentStep) {
        if (i < currentStep) panels[i].classList.add('movingOutBackward');else
        if (i > currentStep) panels[i].classList.add('movingOutFoward');
      } else {
        panels[i].classList.add('movingIn');
      }
    }

    this.updatePanelsContainerHeight();
  }

  setCurrentStep(currentStep) {
    this.currentStep = currentStep;
    this.updatePanelsPosition(currentStep);
  }}


class Wizard {
  constructor(obj) {
    this.wizard = obj;
    this.panels = new Panels(this.wizard);
    this.steps = new Steps(this.wizard);
    this.stepsQuantity = this.steps.getStepsQuantity();
    this.currentStep = this.steps.currentStep;

    this.concludeControlMoveStepMethod = this.steps.handleConcludeStep.bind(this.steps);
    this.wizardConclusionMethod = this.handleWizardConclusion.bind(this);
  }

  updateButtonsStatus() {
    if (this.currentStep === 0)
    this.previousControl.classList.add('disabled');else

    this.previousControl.classList.remove('disabled');
  }

  updtadeCurrentStep(movement) {
    this.currentStep += movement;
    this.steps.setCurrentStep(this.currentStep);
    this.panels.setCurrentStep(this.currentStep);

    this.handleNextStepButton();
    this.updateButtonsStatus();
  }

  
  handleNextStepButton() {
    if (this.currentStep === this.stepsQuantity - 1) {
      this.nextControl.innerHTML = '<svg viewBox="0 0 320 512" style="color: #25c470;"><path fill="currentcolor" d="M438.6 105.4C451.1 117.9 451.1 138.1 438.6 150.6L182.6 406.6C170.1 419.1 149.9 419.1 137.4 406.6L9.372 278.6C-3.124 266.1-3.124 245.9 9.372 233.4C21.87 220.9 42.13 220.9 54.63 233.4L159.1 338.7L393.4 105.4C405.9 92.88 426.1 92.88 438.6 105.4H438.6z"/></svg>'; //BOTAO CONCLUIDO

      this.nextControl.removeEventListener('click', this.nextControlMoveStepMethod);
      this.nextControl.addEventListener('click', this.concludeControlMoveStepMethod);
      this.nextControl.addEventListener('click', this.wizardConclusionMethod);
    } else {
      this.nextControl.innerHTML = '<svg viewBox="0 0 320 512"><path fill="currentcolor" d="M96 480c-8.188 0-16.38-3.125-22.62-9.375c-12.5-12.5-12.5-32.75 0-45.25L242.8 256L73.38 86.63c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0l192 192c12.5 12.5 12.5 32.75 0 45.25l-192 192C112.4 476.9 104.2 480 96 480z"/></svg>'; //BOTAO PROXIMO
      this.nextControl.addEventListener('click', this.nextControlMoveStepMethod);
      this.nextControl.removeEventListener('click', this.concludeControlMoveStepMethod);
      this.nextControl.removeEventListener('click', this.wizardConclusionMethod);
    }
  }

  handleWizardConclusion() {
    this.wizard.classList.add('completed');
  }

  addControls(previousControl, nextControl) {
    this.previousControl = previousControl;
    this.nextControl = nextControl;
    this.previousControlMoveStepMethod = this.moveStep.bind(this, -1);
    this.nextControlMoveStepMethod = this.moveStep.bind(this, 1);

    previousControl.addEventListener('click', this.previousControlMoveStepMethod);
    nextControl.addEventListener('click', this.nextControlMoveStepMethod);

    this.updateButtonsStatus();
  }

  moveStep(movement) {
    if (this.validateMovement(movement)) {
      this.updtadeCurrentStep(movement);
      this.steps.handleStepsClasses(movement);
    } else {
      throw 'This was an invalid movement';
    }
  }

  validateMovement(movement) {
    const fowardMov = movement > 0 && this.currentStep < this.stepsQuantity - 1;
    const backMov = movement < 0 && this.currentStep > 0;

    return fowardMov || backMov;
  }}


let wizardElement = document.getElementById('wizard');
let wizard = new Wizard(wizardElement);
let buttonNext = document.querySelector('.next');
let buttonPrevious = document.querySelector('.previous');

wizard.addControls(buttonPrevious, buttonNext);

function offset(el) {
	var rect = el.getBoundingClientRect(),
	scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
	scrollTop = window.pageYOffset || document.documentElement.scrollTop
	return { top: rect.top + scrollTop, left: rect.left + scrollLeft }
}

let timelineLogoScale = new gsap.timeline()
let timelineInitial = new gsap.timeline()
let timelineCircle = new gsap.timeline()
let timelineLogo = new gsap.timeline()

let $btn = document.querySelector('.btn')

let perimeter = 29 * 2 * Math.PI
let $logoWrapper = document.querySelector('#logo-wrapper')
let $logo = document.querySelector('#logo-wrapper #logo')
let $paths = document.querySelectorAll('#logo path')
let $circleLoader = document.querySelector('#circle-loader')
let $circle = document.querySelector('#circle-loader circle')
let $initialAnimation	= document.querySelector('.initial-animation')

let windowWidth	= window.innerWidth;
let windowHeight = window.innerHeight;

let logoWidth = $logoWrapper.offsetWidth
let logoHeight = $logoWrapper.offsetHeight
let positionLogoTop = offset($logoWrapper).top
let positionLogoLeft = offset($logoWrapper).left

let centerX = (windowWidth - logoWidth) / 2 - positionLogoLeft
let centerY = (windowHeight - logoHeight) / 2 - positionLogoTop

$logoWrapper.style.transform = 'translate('+ centerX +'px, '+ centerY +'px)'

for(let i = 1; i < $paths.length; i++ ) {
	$paths[i].style.strokeDasharray = $paths[i].style.strokeDashoffset = $paths[i].getTotalLength()
}


timelineLogo.add([
	gsap.to($paths[1], 2.1, {strokeDashoffset: 0, delay: .4}),
	gsap.to($paths[2], 0.6, {strokeDashoffset: 0, delay: .7})
])

timelineCircle
	.fromTo($circle, 1.6, 
      {delay: 1.5, strokeDasharray: '0px ' + perimeter + 'px', ease: 'power2.inOut'}, 
      {delay: 0.7, strokeDasharray: perimeter + 'px ' + perimeter + 'px', ease: 'power2.inOut'} 
   )
	.to($circleLoader, 1.3, {rotationZ: '+=360deg'}, '-=1.6' )

timelineLogoScale
	.to($logoWrapper, {scale: 1.6})
	.to($logoWrapper, 0.4, {delay: 0.1, scale: 0.8, ease: 'power4.inOut'})
	.to($logoWrapper, 0.5, {delay: 0.3, scale: 1, ease: 'power4.inOut'})
	.to($logoWrapper, 0.2, {delay: 0.2, scale: 0.9, ease: 'power4.inOut'})
    .to($logoWrapper, 0.2, {delay: 0.1, scale: 1, ease: 'power4.inOut'})    


$btn.addEventListener('click', function() {
  timelineLogoScale.restart()
  timelineInitial.restart()
  timelineCircle.restart()
  timelineLogo.restart()
})
