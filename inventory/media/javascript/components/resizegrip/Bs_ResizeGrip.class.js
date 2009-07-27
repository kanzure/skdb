/********************************************************************************************
* BlueShoes Framework; This file is part of the php application framework.
* NOTE: This code is stripped (obfuscated). To get the clean documented code goto 
*       www.blueshoes.org and register for the free open source *DEVELOPER* version or 
*       buy the commercial version.
*       
*       In case you've already got the developer version, then this is one of the few 
*       packages/classes that is only available to *PAYING* customers.
*       To get it go to www.blueshoes.org and buy a commercial version.
* 
* @copyright www.blueshoes.org
* @author    Samuel Blume <sam at blueshoes dot org>
* @author    Andrej Arn <andrej at blueshoes dot org>
*/
if (!Bs_Objects) {var Bs_Objects = [];};var bs_rg_currentObj;this.bs_rg_resize = function() {
bs_rg_currentObj.resize();}
this.bs_rg_resizeEnd = function() {
bs_rg_currentObj.resizeEnd();}
function Bs_ResizeGrip(containerId) {
var a = arguments;this._containerId = (a.length>1) ? a[1] :  a[0];this._containerElm = document.getElementById(this._containerId);this._objectId;this.maxWidth;this.minWidth = 50;this.maxHeight;this.minHeight = 50;this.gripIcon = '/_bsImages/windows/resizeWindow.gif';this._startX;this._startY;this._containerWidth;this._containerHeight;this.onBeforeResizeStart;this.onAfterResizeStart;this.onBeforeResize;this.onAfterResize;this.onBeforeResizeEnd;this.onAfterResizeEnd;this._drawStyle;this.constructor = function() {
this._id = Bs_Objects.length;Bs_Objects[this._id] = this;this._objectId = "Bs_ResizeGrip_"+this._id;}
this.draw = function() {
var drawStyle = 'inline';if ((this._containerElm.currentStyle.overflow == 'auto') || (this._containerElm.currentStyle.overflow == 'scroll')) {
drawStyle    = 'float';}
var margin = -1;var gripCode = '';gripCode += '<div style="position:absolute; width:20px; height:20px; bottom:0px; right:0px; margin:' + margin + 'px; cursor:se-resize;" onMouseDown="Bs_Objects['+this._id+'].resizeWindowStart(this);" ondragstart="return false;">';gripCode += '<img src="' + this.gripIcon + '">';gripCode += '</div>';if ((this._containerElm.currentStyle.position != 'absolute') && (this._containerElm.currentStyle.position != 'relative')) {
this._containerElm.style.position = 'relative';}
if (drawStyle == 'inline') {
try {
this._containerElm.insertAdjacentHTML('beforeEnd', gripCode);} catch (e) {
drawStyle = 'box';}
}
if (drawStyle == 'box') {
var codeBefore = '<div style="position:absolute; display:inline;">';var codeAfter = gripCode + '<br><div style="display:inline; height:20px;"></div></div>';this._containerElm.outerHTML = codeBefore + this._containerElm.outerHTML + codeAfter;} else if (drawStyle == 'float') {
var margin = 4;var pos = getAbsolutePos(this._containerElm, true);var width  = 20;var height = 20;var left = (pos.x + this._containerElm.clientWidth)  -width;var top  = (pos.y + this._containerElm.clientHeight) -height;var zIndex = (this._containerElm.currentStyle.zIndex > 0) ? (this._containerElm.currentStyle.zIndex +1) : 1;var gripCode = '';gripCode += '<div id="' + this._objectId + '_float" style="position:absolute; z-index:' + zIndex + '; width:' + width + 'px; height:' + height + 'px; left:' + left + 'px; top:' + top + 'px; margin:' + margin + 'px; cursor:se-resize;" onMouseDown="Bs_Objects['+this._id+'].resizeWindowStart(this);" ondragstart="return false;">';gripCode += '<img src="' + this.gripIcon + '">';gripCode += '</div>';this._containerElm.insertAdjacentHTML('afterEnd', gripCode);}
this._drawStyle = drawStyle;}
this._updateFloatingGrip = function() {
var pos = getAbsolutePos(this._containerElm, true);var width  = 20;var height = 20;var grip = document.getElementById(this._objectId + '_float');grip.style.left = (pos.x + this._containerElm.clientWidth)  -width;grip.style.top  = (pos.y + this._containerElm.clientHeight) -height;}
this.resizeWindowStart = function(elm) {
if (!this._fireEvent(this.onBeforeResizeStart)) return;bs_rg_currentObj = this;this._startX = event.clientX;this._startY = event.clientY;this._containerWidth  = this._containerElm.offsetWidth;this._containerHeight = this._containerElm.offsetHeight;if (document.all) {
document.body.attachEvent('onmouseup',   bs_rg_resizeEnd);document.body.attachEvent('onmousemove', bs_rg_resize);} else {
document.addEventListener('mouseup', bs_rg_resizeEnd, false);document.addEventListener('mousemove', bs_rg_resize, false);}
this._fireEvent(this.onAfterResizeStart);}
this.resize = function() {
if (!this._fireEvent(this.onBeforeResize)) return;var diffWidth  = event.clientX - this._startX;var diffHeight = event.clientY - this._startY;var newWidth   = this._containerWidth  + diffWidth;var newHeight  = this._containerHeight + diffHeight;if ((typeof(this.minWidth)  != 'undefined') && (newWidth  < this.minWidth))  newWidth  = this.minWidth;if ((typeof(this.maxWidth)  != 'undefined') && (newWidth  > this.maxWidth))  newWidth  = this.maxWidth;if ((typeof(this.minHeight) != 'undefined') && (newHeight < this.minHeight)) newHeight = this.minHeight;if ((typeof(this.maxHeight) != 'undefined') && (newHeight > this.maxHeight)) newHeight = this.maxHeight;try {
this._containerElm.style.width  = newWidth;this._containerElm.style.height = newHeight;this._containerElm.width        = newWidth;this._containerElm.height       = newHeight;if (this._drawStyle == 'float') this._updateFloatingGrip();} catch (e) {}
this._fireEvent(this.onAfterResize);}
this.resizeEnd = function() {
if (!this._fireEvent(this.onBeforeResizeEnd)) return;if (document.all) {
document.body.detachEvent('onmouseup',   bs_rg_resizeEnd);document.body.detachEvent('onmousemove', bs_rg_resize);} else {
document.removeEventListener('mouseup', bs_rg_resizeEnd, false);document.removeEventListener('mousemove', bs_rg_resize, false);}
this._fireEvent(this.onAfterResizeEnd);}
this._fireEvent = function(ev) {
switch (typeof(ev)) {
case 'function':
var status = ev(this);if (status == false) return false;return true;case 'string':
var status = eval(ev);if (status == false) return false;return true;default:
return true;}
}
this.constructor();}
