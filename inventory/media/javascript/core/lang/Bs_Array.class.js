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
Array.prototype.moveUp = function(key) {
if (key == 0) return this;if (key >= (this.length)) return this;if (key > 1) {
var newArr = this.slice(0, key -1);} else {
var newArr = new Array;}
newArr[newArr.length] = this[key];newArr[newArr.length] = this[key -1];var endArr = this.slice(key +1, this.length);return newArr.concat(endArr);}
Array.prototype.moveDown = function(key) {
if (key >= (this.length -1)) return this;if (key > 0) {
var newArr = this.slice(0, key);} else {
var newArr = new Array;}
newArr[newArr.length] = this[key +1];newArr[newArr.length] = this[key];if (this.length > (key +2)) {
var endArr = this.slice(key +2, this.length);return newArr.concat(endArr);}
return newArr;}
Array.prototype.moveToTop = function(key) {
if (key == 0) return this;if (key >= (this.length)) return this;var startArr  = new Array(this[key]);var middleArr = this.slice(0, key);var endArr    = this.slice(key +1, this.length);return startArr.concat(middleArr, endArr);}
Array.prototype.moveToBottom = function(key) {
if (key >= (this.length -1)) return this;if (key > 0) {
var startArr = this.slice(0, key);} else {
var startArr = new Array;}
var middleArr = this.slice(key +1, this.length);var endArr    = new Array(this[key]);return startArr.concat(middleArr, endArr);}
Array.prototype.indexOf = function(str) {
for(var i=0; i<this.length; i++) {
if (this[i] == str) return i;}
return -1;};Array.prototype.has = function(str) {
return (this.indexOf(str) >= 0);}
Array.prototype.deleteItem = function(i) {
if (i<0 || i>(this.length-1)) return false;if (i == (this.length-1)) {
this.length--;return true;}
for (var i=(i+1); i<this.length; i++) {
this[i-1] = this[i];}
this.length--;return true;};Array.prototype.deleteItemHash = function(key) {
var ret = new Array;for (var k in this) {
if (k != key) ret[k] = this[k];}
return ret;}
function bs_array_maxSizeOfLevel(array, level) {if (!array) return 0;if (array.length == 0) return 0;if (level == 1) return array.length;var ret = 0;for (var i=0; i<array.length; i++) {if (array[i].length > ret) ret = array[i].length;}
return ret;}
function bs_array_toCsv(array, separator) {if (typeof(separator) != 'string') separator = ';';var ret = '';for (var i=0; i<array.length; i++) {var lineA = new Array();for (var j=0; j<array[i].length; j++) {if ((array[i][j]) && (array[i][j]['value'])) {lineA[j] = array[i][j]['value'];}
}
ret += lineA.join(separator) + "\n";}
return ret;}
