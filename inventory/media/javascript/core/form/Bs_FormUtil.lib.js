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
function bsFormToggleCheckbox(formName, fieldName) {
if (document.forms[formName].elements[fieldName].checked) {
document.forms[formName].elements[fieldName].checked = false;} else {
document.forms[formName].elements[fieldName].checked = true;}
}
function bsFormToggleContainer(containerName) {
if (document.all[containerName].style.display == "none") {
document.all[containerName].style.display = "";} else {
document.all[containerName].style.display = "none";}
}
function bsFormCheckMail(url, fieldObj, checkType) {
var fieldName = fieldObj.name;var fieldID   = fieldObj.id;var email     = fieldObj.value;var iFrameObj = document.getElementById('bsMailCheck' + fieldName);url += "?email=" + email + "&checkType=" + checkType;var zeit = new Date();url += "&random=" + zeit.getMilliseconds();iFrameObj.src = url;}
function bsFormJumpToFirstError(fieldName, formName, doSelect) {
if (document.forms[formName].elements[fieldName]) {
if (doSelect && (document.forms[formName].elements[fieldName].value != '')) {
if (document.forms[formName].elements[fieldName].select) {
document.forms[formName].elements[fieldName].select();}
}
if (document.forms[formName].elements[fieldName].focus) {
document.forms[formName].elements[fieldName].focus();}
}
}
function bsFormEnterSubmit(ev, myForm) {
var ev = ('object' == typeof(window.event)) ? window.event : ev;if (ev && ev.keyCode == 13) {
myForm.submit();}
return true;}
function bsFormNoEnter(ev) {
var ev = ('object' == typeof(window.event)) ? window.event : ev;if (ev) return (ev.keyCode != 13);return true;}
function bsFormEnterToTab(ev) {
ev = ('object' == typeof(window.event)) ? window.event : ev;if (ev && ev.keyCode == 13) ev.keyCode = 9;return true;}
function bsFormHandleEnter(ev, functionName) {
var ev = ('object' == typeof(window.event)) ? window.event : ev;if (ev && ev.keyCode == 13) {
return eval(functionName + '();');}
return true;}
function bsFormFieldSetFocusAndSelect(field, force) {
if (typeof(field) == 'string') {
field = document.getElementById(field);}
if (!field) return false;try {
if (force || !field.hasFocus) {
field.focus();field.select();}
} catch (e) {
return false;}
return true;}
function bsFormDoHiddenSubmit(exitScreen, exitAction, nextScreen, nextAction, dataHash, submitToAction) {
var formOutArray =  new Array();var ii=0;formOutArray[ii++] = '<form name="smSubmitForm" action="' + submitToAction + '" method="post">';formOutArray[ii++] = '<input type="hidden" name="bs_todo[nextScreen]" value="' + nextScreen + '">';formOutArray[ii++] = '<input type="hidden" name="bs_todo[exitScreen]" value="' + exitScreen + '">';switch (typeof(nextAction)) {
case 'string':
formOutArray[ii++] = '<input type="hidden" name="bs_todo[nextAction]" value="' + nextAction + '">';break;case 'object':
for (var key in nextAction) {
formOutArray[ii++] = '<input type="hidden" name="bs_todo[nextAction][' + key + ']" value="' + nextAction[key] + '">';}
default:
}
switch (typeof(exitAction)) {
case 'string':
formOutArray[ii++] = '<input type="hidden" name="bs_todo[exitAction]" value="' + exitAction + '">';break;case 'object':
for (var key in exitAction) {
formOutArray[ii++] = '<input type="hidden" name="bs_todo[exitAction][' + key + ']" value="' + exitAction[key] + '">';}
default:
}
dataHash = _recursiveObj2Hash(dataHash);for (var matrixStr in dataHash) {
if (typeof(dataHash[matrixStr]) == 'function') continue;var valStr = bs_filterForHtml(dataHash[matrixStr] + '');formOutArray[ii++] = '<input type="hidden" name="' + "bs_todo[dataHash]" + matrixStr + '" value="' + valStr +  '">';}
formOutArray[ii++] = '</form>';var body = document.getElementsByTagName('body').item(0);body.innerHTML = formOutArray.join('');var form = document.smSubmitForm;form.submit();}
function _recursiveObj2Hash(aObject, matrixStr, flatObjHash) {
if (!flatObjHash) {
flatObjHash = new Object();matrixStr = '';}
if (typeof(aObject) != 'object') {
flatObjHash[matrixStr] = aObject;} else {
for (var key in aObject) {
var newMatrixStr = matrixStr + '['+key+']';_recursiveObj2Hash(aObject[key], newMatrixStr, flatObjHash);}
}
return flatObjHash;}
