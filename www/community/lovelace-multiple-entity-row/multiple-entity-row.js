(()=>{"use strict";var t="[1-9]\\d?",n="\\d\\d",e="[^\\s]+";function i(t,n){for(var e=[],i=0,r=t.length;i<r;i++)e.push(t[i].substr(0,n));return e}var r=function(t){return function(n,e){var i=e[t].map((function(t){return t.toLowerCase()})).indexOf(n.toLowerCase());return i>-1?i:null}};function o(t){for(var n=[],e=1;e<arguments.length;e++)n[e-1]=arguments[e];for(var i=0,r=n;i<r.length;i++){var o=r[i];for(var a in o)t[a]=o[a]}return t}var a=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],c=["January","February","March","April","May","June","July","August","September","October","November","December"],u=i(c,3),s={dayNamesShort:i(a,3),dayNames:a,monthNamesShort:u,monthNames:c,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10?1:0)*t%10]}},f=(o({},s),function(t){return+t-1}),l=[null,t],y=[null,e],d=["isPm",e,function(t,n){var e=t.toLowerCase();return e===n.amPm[0]?0:e===n.amPm[1]?1:null}],h=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(t){var n=(t+"").match(/([+-]|\d\d)/gi);if(n){var e=60*+n[1]+parseInt(n[2],10);return"+"===n[0]?e:-e}return 0}];r("monthNamesShort"),r("monthNames");(function(){try{(new Date).toLocaleDateString("i")}catch(t){return"RangeError"===t.name}})(),function(){try{(new Date).toLocaleString("i")}catch(t){return"RangeError"===t.name}}(),function(){try{(new Date).toLocaleTimeString("i")}catch(t){return"RangeError"===t.name}}();var p=function(t){return t<10?"0"+t:t};function b(t){return t.substr(0,t.indexOf("."))}var v=["closed","locked","off"],m=(new Set(["fan","input_boolean","light","switch","group","automation"]),function(t,n,e,i){i=i||{},e=null==e?{}:e;var r=new Event(n,{bubbles:void 0===i.bubbles||i.bubbles,cancelable:Boolean(i.cancelable),composed:void 0===i.composed||i.composed});return r.detail=e,t.dispatchEvent(r),r});new Set(["call-service","divider","section","weblink","cast","select"]);var g=function(t){m(window,"haptic",t)};function _(t){return(_="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}var w=["entity-id","last-changed","last-updated","last-triggered","position","tilt-position","brightness"],O=function(t){return"object"===_(t)&&!Array.isArray(t)&&!!t},j=function(t){return!t||["unknown","unavailable"].includes(t.state)},k=function(t,n){return n.hide_unavailable&&(j(t)||n.attribute&&void 0===t.attributes[n.attribute])},S=function(t){if(O(t)&&!(t.entity||t.attribute||t.icon))throw new Error("Entity object requires at least one 'entity', 'attribute' or 'icon'.");if("string"==typeof t&&""===t)throw new Error("Entity ID string must not be blank.");if("string"!=typeof t&&!O(t))throw new Error("Entity config must be a valid entity ID string or entity object.")},E=function(t,n){return!1===n.name?null:n.name||(n.entity?t.attributes.friendly_name||(e=t.entity_id).substr(e.indexOf(".")+1):null)||null;var e},P=function(t){return O(null==t?void 0:t.styles)?Object.keys(t.styles).map((function(n){return"".concat(n,": ").concat(t.styles[n],";")})).join(""):""};function x(){var t,n,e=(t=["\n    .icon-small {\n        width: auto;\n    }\n    .entity {\n        text-align: center;\n        cursor: pointer;\n    }\n    .entity span {\n        font-size: 10px;\n        color: var(--secondary-text-color);\n    }\n    .entities-row {\n        flex-direction: row;\n        display: inline-flex;\n        justify-content: space-between;\n        align-items: center;\n    }\n    .entities-row .entity {\n        margin-right: 16px;\n    }\n    .entities-row .entity:last-of-type {\n        margin-right: 0;\n    }\n    .entities-column {\n        flex-direction: column;\n        display: flex;\n        align-items: flex-end;\n        justify-content: space-evenly;\n    }\n    .entities-column .entity div {\n        display: inline-block;\n        vertical-align: middle;\n    }\n"],n||(n=t.slice(0)),Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(n)}})));return x=function(){return e},e}function D(t){return(D="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function I(t,n){var e=Object.keys(t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(t);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(t,n).enumerable}))),e.push.apply(e,i)}return e}function N(t){for(var n=1;n<arguments.length;n++){var e=null!=arguments[n]?arguments[n]:{};n%2?I(Object(e),!0).forEach((function(n){R(t,n,e[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):I(Object(e)).forEach((function(n){Object.defineProperty(t,n,Object.getOwnPropertyDescriptor(e,n))}))}return t}function R(t,n,e){return n in t?Object.defineProperty(t,n,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[n]=e,t}function z(){var t=U(["<hui-warning>\n            ","\n        </hui-warning>"]);return z=function(){return t},t}function M(){var t=U(['<state-badge\n            class="icon-small"\n            .stateObj="','"\n            .overrideIcon="','"\n            .stateColor="','"\n        ></state-badge>']);return M=function(){return t},t}function T(){var t=U(["<hui-timestamp-display\n                .ts=","\n                .format=","\n                .hass=","\n            ></hui-timestamp-display>"]);return T=function(){return t},t}function F(){var t=U(['<ha-entity-toggle .stateObj="','" .hass="','"></ha-entity-toggle>']);return F=function(){return t},t}function L(){var t=U(['<div class="entity" style="','" @click="','">\n            <span>',"</span>\n            <div>","</div>\n        </div>"]);return L=function(){return t},t}function C(){var t=U(["<span>","</span>"]);return C=function(){return t},t}function A(){var t=U(['<div class="state entity" style="','" @click="','">\n            ',"\n            <div>","</div>\n        </div>"]);return A=function(){return t},t}function W(){var t=U([""," ",""]);return W=function(){return t},t}function V(){var t=U(["",""]);return V=function(){return t},t}function H(){var t=U(['<hui-generic-entity-row\n            .hass="','"\n            .config="','"\n            .secondaryText="','"\n        >\n            <div class="','">\n                ',"","\n            </div>\n        </hui-generic-entity-row>"]);return H=function(){return t},t}function J(){var t=U([""]);return J=function(){return t},t}function U(t,n){return n||(n=t.slice(0)),Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(n)}}))}function q(t,n){if(!(t instanceof n))throw new TypeError("Cannot call a class as a function")}function B(t,n){for(var e=0;e<n.length;e++){var i=n[e];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}function Y(t,n){return(Y=Object.setPrototypeOf||function(t,n){return t.__proto__=n,t})(t,n)}function Z(t,n){return!n||"object"!==D(n)&&"function"!=typeof n?function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t):n}function G(t){return(G=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}var K=window.LitElement||Object.getPrototypeOf(customElements.get("hui-masonry-view")||customElements.get("hui-view")),Q=K.prototype,X=Q.html,$=Q.css;console.info("%c MULTIPLE-ENTITY-ROW %c 4.1.1 ","color: cyan; background: black; font-weight: bold;","color: darkblue; background: white; font-weight: bold;");var tt=function(t){!function(t,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(n&&n.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),n&&Y(t,n)}(c,t);var n,e,i,r,o,a=(r=c,o=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(t){return!1}}(),function(){var t,n=G(r);if(o){var e=G(this).constructor;t=Reflect.construct(n,arguments,e)}else t=n.apply(this,arguments);return Z(this,t)});function c(){return q(this,c),a.apply(this,arguments)}return n=c,i=[{key:"properties",get:function(){return{_hass:Object,config:Object,stateObj:Object}}},{key:"styles",get:function(){return function(t){return t(x())}($)}}],(e=[{key:"setConfig",value:function(t){if(!t||!t.entity)throw new Error("Please define a main entity.");t.entities&&t.entities.forEach((function(t){return S(t)})),t.secondary_info&&S(t.secondary_info),this.entityIds=function(t){var n,e;return[t.entity,null===(n=t.secondary_info)||void 0===n?void 0:n.entity].concat(null===(e=t.entities)||void 0===e?void 0:e.map((function(t){return"string"==typeof t?t:t.entity}))).filter((function(t){return t}))}(t),this.onRowClick=this.clickHandler(t.entity,t.tap_action),this.config=t}},{key:"shouldUpdate",value:function(t){return function(t,n){if(n.has("config"))return!0;var e=n.get("_hass");return!!e&&t.entityIds.some((function(n){return e.states[n]!==t._hass.states[n]}))}(this,t)}},{key:"render",value:function(){var t=this;return this._hass&&this.config?this.stateObj?X(H(),this._hass,this.config,this.renderSecondaryInfo(),this.config.column?"entities-column":"entities-row",this.entities.map((function(n){return t.renderEntity(n.stateObj,n)})),this.renderMainEntity()):this.renderWarning():X(J())}},{key:"renderSecondaryInfo",value:function(){if(!this.config.secondary_info||"string"==typeof(t=this.config.secondary_info)&&w.includes(t)||k(this.info,this.config.secondary_info))return null;var t;if("string"==typeof this.config.secondary_info)return X(V(),this.config.secondary_info);var n=E(this.info,this.config.secondary_info);return X(W(),n,this.renderValue(this.info,this.config.secondary_info))}},{key:"renderMainEntity",value:function(){return!1===this.config.show_state?null:X(A(),P(this.config),this.onRowClick,this.config.state_header&&X(C(),this.config.state_header),this.renderValue(this.stateObj,this.config))}},{key:"renderEntity",value:function(t,n){if(!t||k(t,n))return null;var e=this.clickHandler(t.entity_id,n.tap_action);return X(L(),P(n),e,E(t,n),n.icon?this.renderIcon(t,n):this.renderValue(t,n))}},{key:"renderValue",value:function(t,n){return function(t,n){return!0===n.toggle&&!j(t)}(t,n)?X(F(),t,this._hass):n.format?this.renderFormat(t,n):function(t,n,e){if(j(n))return t.localize("state.default.".concat(n.state));if(e.attribute)return e.attribute in n.attributes?"".concat(n.attributes[e.attribute]).concat(e.unit?" ".concat(e.unit):""):t.localize("state.default.unavailable");if(!1!==e.unit&&(e.unit||n.attributes.unit_of_measurement))return"".concat(n.state," ").concat(e.unit||n.attributes.unit_of_measurement);var i=b(n.entity_id);return n.attributes.device_class&&t.localize("component.".concat(i,".state.").concat(n.attributes.device_class,".").concat(n.state))||t.localize("component.".concat(i,".state._.").concat(n.state))||n.state}(this._hass,t,n)}},{key:"renderFormat",value:function(t,n){var e,i,r,o,a=function(t,n){return void 0!==n.attribute?t.attributes[n.attribute]:t.state}(t,n);if(["relative","total","date","time","datetime"].includes(n.format)){var c=new Date(a);return c instanceof Date&&!isNaN(c.getTime())?X(T(),c,n.format,this._hass):a}if(isNaN(parseFloat(a))||!isFinite(a))return a;if("brightness"===n.format)return"".concat(Math.round(a/255*100)," %");if("duration"===n.format)return e=a,i=Math.floor(e/3600),r=Math.floor(e%3600/60),o=Math.floor(e%3600%60),i>0?i+":"+p(r)+":"+p(o):r>0?r+":"+p(o):o>0?""+o:null;if(n.format.startsWith("precision")){var u=function(t,n){return void 0!==n.attribute?n.unit:n.unit||t.attributes.unit_of_measurement}(t,n),s=parseInt(n.format.slice(-1),10);return"".concat(parseFloat(a).toFixed(s)).concat(u?" ".concat(u):"")}return a}},{key:"renderIcon",value:function(t,n){return X(M(),t,!0===n.icon?t.attributes.icon||null:n.icon,n.state_color)}},{key:"renderWarning",value:function(){return X(z(),this._hass.localize("ui.panel.lovelace.warning.entity_not_found","entity",this.config.entity))}},{key:"clickHandler",value:function(t,n){var e=this;return function(){return function(t,n,e,i,r){var o;if(e.tap_action&&(o=e.tap_action),o||(o={action:"more-info"}),!o.confirmation||o.confirmation.exemptions&&o.confirmation.exemptions.some((function(t){return t.user===n.user.id}))||confirm(o.confirmation.text||"Are you sure you want to "+o.action+"?"))switch(o.action){case"more-info":(o.entity||e.entity||e.camera_image)&&(m(t,"hass-more-info",{entityId:o.entity?o.entity:e.entity?e.entity:e.camera_image}),o.haptic&&g(o.haptic));break;case"navigate":o.navigation_path&&(function(t,n,e){void 0===e&&(e=!1),e?history.replaceState(null,"",n):history.pushState(null,"",n),m(window,"location-changed",{replace:e})}(0,o.navigation_path),o.haptic&&g(o.haptic));break;case"url":o.url_path&&window.open(o.url_path),o.haptic&&g(o.haptic);break;case"toggle":e.entity&&(function(t,n){(function(t,n,e){void 0===e&&(e=!0);var i,r=b(n),o="group"===r?"homeassistant":r;switch(r){case"lock":i=e?"unlock":"lock";break;case"cover":i=e?"open_cover":"close_cover";break;default:i=e?"turn_on":"turn_off"}t.callService(o,i,{entity_id:n})})(t,n,v.includes(t.states[n].state))}(n,e.entity),o.haptic&&g(o.haptic));break;case"call-service":if(!o.service)return;var a=o.service.split(".",2),c=a[0],u=a[1],s=Object.assign({},o.service_data);"entity"===s.entity_id&&(s.entity_id=e.entity),n.callService(c,u,s),o.haptic&&g(o.haptic)}}(e,e._hass,{entity:t,tap_action:n})}}},{key:"hass",set:function(t){var n,e,i,r=this;this._hass=t,t&&this.config&&(this.stateObj=t.states[this.config.entity],O(this.config.secondary_info)&&(this.info=null!==(i=t.states[this.config.secondary_info.entity])&&void 0!==i?i:this.stateObj),this.entities=null!==(n=null===(e=this.config.entities)||void 0===e?void 0:e.map((function(n){var e="string"==typeof n?{entity:n}:n;return N(N({},e),{},{stateObj:e.entity?t.states[e.entity]:r.stateObj})})))&&void 0!==n?n:[])}}])&&B(n.prototype,e),i&&B(n,i),c}(K);customElements.define("multiple-entity-row",tt)})();