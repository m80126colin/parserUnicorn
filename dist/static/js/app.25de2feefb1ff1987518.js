webpackJsonp([2,0],{0:function(t,e,a){"use strict";function n(t){return t&&t.__esModule?t:{default:t}}var s=a(212),r=n(s),i=a(211),o=n(i),u=a(195),d=n(u);r.default.use(o.default);var l=a(13),c=new o.default({routes:l});new r.default({router:c,template:"<App/>",components:{App:d.default}}).$mount("#app")},13:function(t,e,a){"use strict";function n(t){return t&&t.__esModule?t:{default:t}}var s=a(197),r=n(s),i=a(196),o=n(i),u=a(201),d=n(u),l=a(198),c=(n(l),a(200)),f=n(c),p={template:"<div></div>"};t.exports=[{path:"/",name:"首頁",component:p},{path:"/parser",name:"資料蒐集",component:d.default},{path:"/onepage",name:"單頁資料擷取",component:f.default},{path:"/cloud",name:"文字雲",component:r.default},{path:"/association",name:"關聯分析",component:o.default}]},139:function(t,e,a){"use strict";function n(t){return t&&t.__esModule?t:{default:t}}Object.defineProperty(e,"__esModule",{value:!0});var s=a(7),r=n(s),i=a(4),o=n(i),u=a(199),d=n(u);a(149),a(154);var l={record:0};window._=o.default;var c=function(t,e){return $.ajax({type:"POST",url:t,data:(0,r.default)(e),contentType:"application/json",dataType:"json"})};e.default={name:"app",components:{Navbar:d.default},data:function(){return{store:{token:""},records:{header:["","文章連結","分享數","按讚數","留言數"],size:10,data:[]}}},methods:{addRecord:function(t){var e=this,a=function(t){return{state:1,result:t}},n=function(){return{state:-1}},s={id:l.record++,post:{state:0,result:{},api:"/api/post/id"},submits:[{state:0,result:{},api:"/api/post/shares"},{state:0,result:{},api:"/api/post/likes"},{state:0,result:{},api:"/api/post/comments"}]};e.records.data=o.default.concat(s,e.records.data),c(s.post.api,{token:e.store.token,url:t}).done(function(t){o.default.assign(s.post,a(t)),o.default.forEach(s.submits,function(s){c(s.api,{token:e.store.token,postid:t.postid}).done(function(t){o.default.assign(s,a(t))}).fail(function(t){o.default.assign(s,n())})})}).fail(function(t){o.default.assign(s.post,n()),o.default.forEach(s.submits,function(t){o.default.assign(t,n()),window.console.log(t.state)})})},setRecordPageSize:function(t){this.records.size=t},setToken:function(t){this.store.token=t}}}},140:function(t,e,a){"use strict";function n(t){return t&&t.__esModule?t:{default:t}}Object.defineProperty(e,"__esModule",{value:!0});var s=a(3),r=n(s),i=1;e.default={data:function(){return{files:[{id:0}],link:"",link2:"",result:[]}},name:"association",methods:{addFile:function(t){var e=this;e.files.push({id:i}),i++},delFile:function(t){var e=this,a=(0,r.default)(t.target).attr("data-id");e.files.splice(a,1)},associHandler:function(t){var e=this,a=new FormData((0,r.default)("#form")[0]);r.default.ajax({type:"POST",url:"/api/associ",data:a,processData:!1,contentType:!1}).done(function(t){e.link=t.link,e.link2=t.link2,e.result=JSON.parse(t.list)})}}}},141:function(t,e,a){"use strict";function n(t){return t&&t.__esModule?t:{default:t}}Object.defineProperty(e,"__esModule",{value:!0});var s=a(4),r=n(s),i=a(3),o=n(i),u=a(155),d=n(u),l=a(138),c=n(l);window.stat=d.default,e.default={name:"cloud",data:function(){return{width:1e3,link:"",will:"",cloudData:[]}},computed:{height:function(){return Math.floor(.75*this.width)},wont:function(){return(this.will||"").trim().split("\n").map(function(t){return t.trim().split(/\s+/)})}},watch:{cloudData:function(t){if(Array.isArray(t)&&0!==t.length){var e=this,a=1e4,n=r.default.chain(t).map(function(t){return"number"!=typeof t[1]&&(t[1]=0),t}).sort(function(t,e){return e[1]-t[1]}).take(a).value(),s=r.default.map(n,function(t){return t[1]}),i=d.default.mean(s),u=d.default.standardDeviation(s),l=(0,o.default)("#cloud").width()/e.width,f=function(t){return d.default.zScore(t,i,u)||0},p=f(d.default.max(s));(0,c.default)(document.getElementById("cloud"),{list:n,fontFamily:"Times, serif, 標楷體",rotateRatio:.5,gridSize:Math.round(6*l),weightFactor:function(t){return 12*l*(7*f(t)/p+.75)}})}}},methods:{cloudHandler:function(t){var e=this,a=new FormData((0,o.default)("#form")[0]);o.default.ajax({type:"POST",url:"/api/cloud",data:a,processData:!1,contentType:!1}).done(function(t){var a=JSON.parse(t.list);e.link=t.link,e.cloudData=a})},visualizeData:function(t){var e=this;e.cloudData=r.default.map(e.wont,function(t){return[t[0],parseInt(t[1])||0]})}}}},142:function(t,e,a){"use strict";function n(t){return t&&t.__esModule?t:{default:t}}Object.defineProperty(e,"__esModule",{value:!0});var s=a(7),r=n(s),i=a(4),o=n(i),u=a(3),d=n(u),l=0;window.$=window.jQuery=d.default,e.default={name:"like",data:function(){return{token:"",datarows:[]}},created:function(){this.addRow()},filters:{showState:function(t){return t===-1?"初始化":1===t?"處理中":2===t?"處理錯誤":"處理完成"},countLength:function(t){return t?t.length:""}},methods:{addRow:function(t){this.datarows.push({id:l,url:"",result:{state:-1,id:""}}),l++},deleteRow:function(t){var e=(0,d.default)(t.target).attr("data-id");this.datarows.splice(e,1)},likesHandler:function(t){var e=this,a=(0,d.default)(t.target).attr("data-id"),n=e.datarows[a];return o.default.assign(n.result,{state:1}),d.default.ajax({type:"POST",url:"/api/likes",data:(0,r.default)({token:e.token,url:n.url}),contentType:"application/json",dataType:"json"}).done(function(t){o.default.assign(n.result,t),o.default.assign(n.result,{state:0})}).fail(function(t){o.default.assign(n.result,{state:2})})},downloadData:function(t){var e=(0,d.default)(t.target).attr("id"),a=this.datarows[e].result,n="/downloads/"+a.link;window.open(n,"_blank")},facebookLink:function(t){var e=(0,d.default)(t.target).attr("id"),a=this.datarows[e].result,n="https://www.facebook.com/"+a.id;window.open(n,"_blank")}}}},143:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=a(13);e.default={name:"menu",data:function(){return{routes:n}}}},144:function(t,e,a){"use strict";function n(t){return t&&t.__esModule?t:{default:t}}Object.defineProperty(e,"__esModule",{value:!0});var s=a(202),r=n(s);e.default={name:"onepage",props:["appdata"],components:{Record:r.default},data:function(){return{url:""}},computed:{token:function(){return this.appdata.store.token},records:function(){return this.appdata.records.data}},methods:{recordSubmit:function(t){var e=this;e.$emit("addRecord",e.url),e.url=""}}}},145:function(t,e,a){"use strict";function n(t){return t&&t.__esModule?t:{default:t}}Object.defineProperty(e,"__esModule",{value:!0});var s=a(7),r=n(s),i=a(3),o=n(i),u=a(1),d=n(u),l=[{id:"token",type:"text",name:"Token",after:'<a target="_blank" href="https://developers.facebook.com/tools/explorer/">到此領取 token</a>'},{id:"url",type:"text",name:"粉絲專頁連結"},{id:"since",type:"date",name:"開始時間"},{id:"until",type:"date",name:"結束時間"}];e.default={name:"parser",props:["appdata"],data:function(){return{fields:l,fetch:!1,result:[]}},methods:{getTime:function(t){return(0,d.default)(t).format("YYYY/MM/DD HH:mm:ss ZZ")},getAllPosts:function(t){var e=this,a=l.map(function(t){return t.id}),n={};a.forEach(function(t){n[t]=(0,o.default)("#"+t).val()}),o.default.ajax({type:"POST",url:"/api/allposts",data:(0,r.default)(n),contentType:"application/json",dataType:"json"}).done(function(t){e.fetch=!0,e.result=t})},downloadListener:function(t){var e=(0,o.default)(t.target).attr("data-id"),a="/api/allcomments/"+e+"?token="+(0,o.default)("#token").val();window.open(a,"_blank")}}}},146:function(t,e,a){"use strict";function n(t){return t&&t.__esModule?t:{default:t}}Object.defineProperty(e,"__esModule",{value:!0});var s=a(4),r=n(s),i=a(3),o=n(i);e.default={name:"record",props:["appdata"],data:function(){return{page:0}},computed:{records:function(){var t=this.appdata.records;return r.default.chunk(t.data,t.size)},header:function(){return this.appdata.records.header}},methods:{facebookLink:function(t){return"https://www.facebook.com/"+t},downloadLink:function(t){return"/api/download/"+t},toPage:function(t){var e=this;e.page=(0,o.default)(t.target).data("id")}}}},149:function(t,e){},150:function(t,e){},151:function(t,e){},152:function(t,e){},153:function(t,e,a){function n(t){return a(s(t))}function s(t){return r[t]||function(){throw new Error("Cannot find module '"+t+"'.")}()}var r={"./af":14,"./af.js":14,"./ar":20,"./ar-dz":15,"./ar-dz.js":15,"./ar-ly":16,"./ar-ly.js":16,"./ar-ma":17,"./ar-ma.js":17,"./ar-sa":18,"./ar-sa.js":18,"./ar-tn":19,"./ar-tn.js":19,"./ar.js":20,"./az":21,"./az.js":21,"./be":22,"./be.js":22,"./bg":23,"./bg.js":23,"./bn":24,"./bn.js":24,"./bo":25,"./bo.js":25,"./br":26,"./br.js":26,"./bs":27,"./bs.js":27,"./ca":28,"./ca.js":28,"./cs":29,"./cs.js":29,"./cv":30,"./cv.js":30,"./cy":31,"./cy.js":31,"./da":32,"./da.js":32,"./de":34,"./de-at":33,"./de-at.js":33,"./de.js":34,"./dv":35,"./dv.js":35,"./el":36,"./el.js":36,"./en-au":37,"./en-au.js":37,"./en-ca":38,"./en-ca.js":38,"./en-gb":39,"./en-gb.js":39,"./en-ie":40,"./en-ie.js":40,"./en-nz":41,"./en-nz.js":41,"./eo":42,"./eo.js":42,"./es":44,"./es-do":43,"./es-do.js":43,"./es.js":44,"./et":45,"./et.js":45,"./eu":46,"./eu.js":46,"./fa":47,"./fa.js":47,"./fi":48,"./fi.js":48,"./fo":49,"./fo.js":49,"./fr":52,"./fr-ca":50,"./fr-ca.js":50,"./fr-ch":51,"./fr-ch.js":51,"./fr.js":52,"./fy":53,"./fy.js":53,"./gd":54,"./gd.js":54,"./gl":55,"./gl.js":55,"./he":56,"./he.js":56,"./hi":57,"./hi.js":57,"./hr":58,"./hr.js":58,"./hu":59,"./hu.js":59,"./hy-am":60,"./hy-am.js":60,"./id":61,"./id.js":61,"./is":62,"./is.js":62,"./it":63,"./it.js":63,"./ja":64,"./ja.js":64,"./jv":65,"./jv.js":65,"./ka":66,"./ka.js":66,"./kk":67,"./kk.js":67,"./km":68,"./km.js":68,"./ko":69,"./ko.js":69,"./ky":70,"./ky.js":70,"./lb":71,"./lb.js":71,"./lo":72,"./lo.js":72,"./lt":73,"./lt.js":73,"./lv":74,"./lv.js":74,"./me":75,"./me.js":75,"./mi":76,"./mi.js":76,"./mk":77,"./mk.js":77,"./ml":78,"./ml.js":78,"./mr":79,"./mr.js":79,"./ms":81,"./ms-my":80,"./ms-my.js":80,"./ms.js":81,"./my":82,"./my.js":82,"./nb":83,"./nb.js":83,"./ne":84,"./ne.js":84,"./nl":86,"./nl-be":85,"./nl-be.js":85,"./nl.js":86,"./nn":87,"./nn.js":87,"./pa-in":88,"./pa-in.js":88,"./pl":89,"./pl.js":89,"./pt":91,"./pt-br":90,"./pt-br.js":90,"./pt.js":91,"./ro":92,"./ro.js":92,"./ru":93,"./ru.js":93,"./se":94,"./se.js":94,"./si":95,"./si.js":95,"./sk":96,"./sk.js":96,"./sl":97,"./sl.js":97,"./sq":98,"./sq.js":98,"./sr":100,"./sr-cyrl":99,"./sr-cyrl.js":99,"./sr.js":100,"./ss":101,"./ss.js":101,"./sv":102,"./sv.js":102,"./sw":103,"./sw.js":103,"./ta":104,"./ta.js":104,"./te":105,"./te.js":105,"./tet":106,"./tet.js":106,"./th":107,"./th.js":107,"./tl-ph":108,"./tl-ph.js":108,"./tlh":109,"./tlh.js":109,"./tr":110,"./tr.js":110,"./tzl":111,"./tzl.js":111,"./tzm":113,"./tzm-latn":112,"./tzm-latn.js":112,"./tzm.js":113,"./uk":114,"./uk.js":114,"./uz":115,"./uz.js":115,"./vi":116,"./vi.js":116,"./x-pseudo":117,"./x-pseudo.js":117,"./yo":118,"./yo.js":118,"./zh-cn":119,"./zh-cn.js":119,"./zh-hk":120,"./zh-hk.js":120,"./zh-tw":121,"./zh-tw.js":121};n.keys=function(){return Object.keys(r)},n.resolve=s,t.exports=n,n.id=153},195:function(t,e,a){var n,s;a(150),n=a(139);var r=a(203);s=n=n||{},"object"!=typeof n.default&&"function"!=typeof n.default||(s=n=n.default),"function"==typeof s&&(s=s.options),s.render=r.render,s.staticRenderFns=r.staticRenderFns,t.exports=n},196:function(t,e,a){var n,s;n=a(140);var r=a(204);s=n=n||{},"object"!=typeof n.default&&"function"!=typeof n.default||(s=n=n.default),"function"==typeof s&&(s=s.options),s.render=r.render,s.staticRenderFns=r.staticRenderFns,t.exports=n},197:function(t,e,a){var n,s;n=a(141);var r=a(207);s=n=n||{},"object"!=typeof n.default&&"function"!=typeof n.default||(s=n=n.default),"function"==typeof s&&(s=s.options),s.render=r.render,s.staticRenderFns=r.staticRenderFns,t.exports=n},198:function(t,e,a){var n,s;n=a(142);var r=a(210);s=n=n||{},"object"!=typeof n.default&&"function"!=typeof n.default||(s=n=n.default),"function"==typeof s&&(s=s.options),s.render=r.render,s.staticRenderFns=r.staticRenderFns,t.exports=n},199:function(t,e,a){var n,s;a(152),n=a(143);var r=a(208);s=n=n||{},"object"!=typeof n.default&&"function"!=typeof n.default||(s=n=n.default),"function"==typeof s&&(s=s.options),s.render=r.render,s.staticRenderFns=r.staticRenderFns,t.exports=n},200:function(t,e,a){var n,s;n=a(144);var r=a(209);s=n=n||{},"object"!=typeof n.default&&"function"!=typeof n.default||(s=n=n.default),"function"==typeof s&&(s=s.options),s.render=r.render,s.staticRenderFns=r.staticRenderFns,t.exports=n},201:function(t,e,a){var n,s;a(151),n=a(145);var r=a(205);s=n=n||{},"object"!=typeof n.default&&"function"!=typeof n.default||(s=n=n.default),"function"==typeof s&&(s=s.options),s.render=r.render,s.staticRenderFns=r.staticRenderFns,t.exports=n},202:function(t,e,a){var n,s;n=a(146);var r=a(206);s=n=n||{},"object"!=typeof n.default&&"function"!=typeof n.default||(s=n=n.default),"function"==typeof s&&(s=s.options),s.render=r.render,s.staticRenderFns=r.staticRenderFns,t.exports=n},203:function(t,e){t.exports={render:function(){var t=this,e=(t.$createElement,t._c);return e("div",{staticClass:"ui centered grid",attrs:{id:"app"}},[e("div",{staticClass:"two wide column"}),t._v(" "),e("div",{staticClass:"twelve wide column"},[e("navbar"),t._v(" "),e("router-view",{attrs:{appdata:t.$data},on:{addRecord:t.addRecord,setRecordPageSize:t.setRecordPageSize,setToken:t.setToken}})]),t._v(" "),e("div",{staticClass:"two wide column"})])},staticRenderFns:[]}},204:function(t,e){t.exports={render:function(){var t=this,e=(t.$createElement,t._c);return e("section",{attrs:{id:"association"}},[e("form",{staticClass:"ui form",attrs:{id:"form",method:"post",enctype:"multipart/form-data"}},[t._l(t.files,function(a,n){return e("div",{key:a.id,staticClass:"inline field",attrs:{"data-tag":a.id}},[e("label",{attrs:{for:"file"+n}},[t._v("檔案 "+t._s(n))]),t._v(" "),e("input",{staticClass:"pure-input-1-2",attrs:{id:"file"+n,type:"file",name:"file"+n}}),t._v(" "),e("button",{staticClass:"ui button",attrs:{"data-id":n},on:{click:function(e){e.preventDefault(),t.delFile(e)}}},[t._v("刪除")])])}),t._v(" "),e("div",{staticClass:"field"},[e("button",{staticClass:"ui button",on:{click:function(e){e.preventDefault(),t.addFile(e)}}},[t._v("新增")]),t._v(" "),e("button",{staticClass:"ui primary button",on:{click:function(e){e.preventDefault(),t.associHandler(e)}}},[t._v("送出")])]),t._v(" "),e("div",{staticClass:"ui basic segment",attrs:{id:"result"}},[t.link?e("div",{attrs:{id:"apriori"}},[e("a",{staticClass:"ui button",attrs:{target:"_blank",href:t.link}},[t._v("下載關聯矩陣")])]):t._e(),t._v(" "),t.link2?e("div",{attrs:{id:"apriori"}},[e("a",{staticClass:"ui button",attrs:{target:"_blank",href:t.link2}},[t._v("下載關聯規則")])]):t._e(),t._v(" "),t.result.length?e("table",{staticClass:"ui table"},[t._m(0),t._v(" "),e("tbody",t._l(t.result,function(a){return e("tr",[e("td",[t._v(t._s(a.itema)+" => "+t._s(a.itemb))]),t._v(" "),e("td",[t._v(t._s(a.support))]),t._v(" "),e("td",[t._v(t._s(a.confident))])])}))]):t._e()])],!0)])},staticRenderFns:[function(){var t=this,e=(t.$createElement,t._c);return e("thead",[e("tr",[e("th",[t._v("Rules")]),t._v(" "),e("th",[t._v("Support")]),t._v(" "),e("th",[t._v("Confident")])])])}]}},205:function(t,e){t.exports={render:function(){var t=this,e=(t.$createElement,t._c);return e("section",{attrs:{id:"parser"}},[t._m(0),t._v(" "),e("article",{staticClass:"ui basic segment"},[t._m(1),t._v(" "),e("form",{staticClass:"ui equal width form",attrs:{id:"form"}},[e("div",{staticClass:"fields"},t._l(t.fields,function(a){return e("div",{staticClass:"field"},[e("label",{attrs:{for:a.id}},[t._v(t._s(a.name))]),t._v(" "),e("input",{attrs:{type:a.type,id:a.id}}),t._v(" "),"after"in a?e("label",{attrs:{for:a.id},domProps:{innerHTML:t._s(a.after)}}):t._e()])})),t._v(" "),e("div",{staticClass:"field"},[e("button",{staticClass:"ui primary button",on:{click:function(e){e.preventDefault(),t.getAllPosts(e)}}},[t._v("送出")])])]),t._v(" "),t.fetch?e("div",{staticClass:"ui basic segment",attrs:{id:"msg"}},[e("p",[t._v("共有 "+t._s(t.result.length)+" 筆結果。")])]):t._e(),t._v(" "),t.result.length?e("table",{staticClass:"ui table",attrs:{id:"result"}},[t._m(2),t._v(" "),e("tbody",t._l(t.result,function(a,n){return e("tr",{key:n},[e("td",[t._v(t._s(n))]),t._v(" "),e("td",[t._v(t._s(a.id))]),t._v(" "),e("td",[t._v(t._s(t.getTime(a.created_time)))]),t._v(" "),e("td",[t._v(t._s(a.likes.summary.total_count))]),t._v(" "),e("td",[t._v(t._s(a.comments.summary.total_count))]),t._v(" "),e("td",[t._v(t._s(a.shares.count))]),t._v(" "),e("td",[e("a",{staticClass:"ui button",attrs:{target:"_blank",href:"https://www.facebook.com/"+a.id}},[t._v("連結")])]),t._v(" "),e("td",[e("button",{staticClass:"ui primary button parser-download",attrs:{"data-id":a.id},on:{click:t.downloadListener}},[t._v("下載")])])])}))]):t._e()])])},staticRenderFns:[function(){var t=this,e=(t.$createElement,t._c);return e("header",{staticClass:"ui header"},[e("h1",[t._v("資料蒐集")])])},function(){var t=this,e=(t.$createElement,t._c);return e("header",{staticClass:"ui dividing header"},[e("h2",[t._v("粉絲專頁")])])},function(){var t=this,e=(t.$createElement,t._c);return e("thead",[e("tr",[e("th",[t._v("#")]),t._v(" "),e("th",[t._v("id")]),t._v(" "),e("th",[t._v("create time")]),t._v(" "),e("th",[t._v("like count")]),t._v(" "),e("th",[t._v("comment count")]),t._v(" "),e("th",[t._v("share count")]),t._v(" "),e("th",[t._v("Link")]),t._v(" "),e("th",[t._v("Download")])])])}]}},206:function(t,e){t.exports={render:function(){var t=this,e=(t.$createElement,t._c);return e("table",{staticClass:"ui celled definition table"},[e("thead",[e("tr",t._l(t.header,function(a){return e("th",[t._v(t._s(a))])}))]),t._v(" "),e("tbody",t._l(t.records[t.page],function(a){return e("tr",[e("td",[t._v(t._s(a.id))]),t._v(" "),1===a.post.state?e("td",[e("a",{attrs:{target:"_blank",href:t.facebookLink(a.post.result.postid)}},[t._v("\r\n          "+t._s(a.post.result.postid)+"\r\n        ")])]):a.post.state===-1?e("td",{staticClass:"negative"},[t._v("失敗")]):e("td",[e("div",{staticClass:"ui loading basic segment"})]),t._v(" "),t._v(" "),t._l(a.submits,function(a){return 1===a.state?e("td",[t._v("\r\n        "+t._s(a.result.count)+"\r\n        "),a.result.link?e("a",{staticClass:"ui tiny primary button",attrs:{target:"_blank",href:t.downloadLink(a.result.link)}},[t._v("下載")]):t._e()]):a.state===-1?e("td",{staticClass:"negative"},[t._v("失敗")]):e("td",[e("div",{staticClass:"ui loading basic segment"})])}),t._v(" "),t._v(" ")],!0)})),t._v(" "),e("tfoot",[e("tr",[e("th",{attrs:{colspan:t.header.length}},[e("div",{staticClass:"ui right floated pagination menu"},t._l(t.records,function(a,n){return e("a",{staticClass:"item",attrs:{"data-id":n},on:{click:t.toPage}},[t._v(t._s(n+1))])}))])])])])},staticRenderFns:[]}},207:function(t,e){t.exports={render:function(){var t=this,e=(t.$createElement,t._c);return e("section",{staticClass:"cloud",attrs:{id:"cloud"}},[e("form",{staticClass:"ui form",attrs:{id:"form",method:"post",enctype:"multipart/form-data"},on:{submit:function(e){e.preventDefault(),t.cloudHandler(e)}}},[t._m(0)]),t._v(" "),e("div",{directives:[{name:"show",rawName:"v-show",value:t.link,expression:"link"}],staticClass:"ui basic segment",attrs:{id:"count"}},[e("a",{staticClass:"ui button",attrs:{target:"_blank",href:t.link}},[t._v("下載")])]),t._v(" "),t._e(),t._v(" "),e("div",{staticClass:"ui basic segment canvas-container"},[e("canvas",{attrs:{id:"cloud",width:t.width,height:t.height}})])])},staticRenderFns:[function(){var t=this,e=(t.$createElement,t._c);return e("div",{staticClass:"inline field"},[e("input",{attrs:{id:"data",type:"file",name:"data"}}),t._v(" "),e("button",{staticClass:"ui primary button",attrs:{type:"submit"}},[t._v("上傳")])])}]}},208:function(t,e){t.exports={render:function(){var t=this,e=(t.$createElement,t._c);return e("nav",{staticClass:"ui menu",attrs:{id:"navbar"}},t._l(t.routes,function(a){return e("router-link",{staticClass:"item",attrs:{to:a.path}},[t._v("\r\n  "+t._s(a.name)+"\r\n  ")])}))},staticRenderFns:[]}},209:function(t,e){t.exports={render:function(){var t=this,e=(t.$createElement,t._c);return e("section",{attrs:{id:"onepage"}},[t._m(0),t._v(" "),e("article",{staticClass:"ui basic segment"},[t._m(1),t._v(" "),e("form",{staticClass:"ui equal width form"},[e("div",{staticClass:"fields"},[e("div",{staticClass:"field"},[e("label",{attrs:{for:"token"}},[t._v("Token")]),t._v(" "),e("input",{attrs:{type:"text",name:"token"},domProps:{value:t.appdata.store.token},on:{input:function(e){t.$emit("setToken",e.target.value)}}}),t._v(" "),t._m(2)]),t._v(" "),e("div",{staticClass:"field"},[e("label",{attrs:{for:"url"}},[t._v("文章連結")]),t._v(" "),e("input",{directives:[{name:"model",rawName:"v-model",value:t.url,expression:"url"}],attrs:{type:"text",name:"url"},domProps:{value:t._s(t.url)},on:{input:function(e){e.target.composing||(t.url=e.target.value)}}})])]),t._v(" "),e("div",{staticClass:"field"},[e("button",{staticClass:"ui primary button",attrs:{type:"submit"},on:{click:function(e){e.preventDefault(),t.recordSubmit(e)}}},[t._v("送出")]),t._v(" "),e("button",{staticClass:"ui button",attrs:{type:"reset"}},[t._v("清除")])])])]),t._v(" "),t.records.length?e("article",[t._m(3),t._v(" "),e("record",{attrs:{appdata:t.appdata}})]):t._e()])},staticRenderFns:[function(){var t=this,e=(t.$createElement,t._c);return e("header",{staticClass:"ui header"},[e("h1",[t._v("單頁資料擷取")])])},function(){var t=this,e=(t.$createElement,t._c);return e("header",{staticClass:"ui dividing header"},[e("h2",[t._v("單頁連結")])])},function(){var t=this,e=(t.$createElement,t._c);return e("label",{attrs:{for:"token"}},[e("a",{attrs:{target:"_blank",href:"https://developers.facebook.com/tools/explorer/"}},[t._v("到此領取 token")])])},function(){var t=this,e=(t.$createElement,t._c);return e("header",{staticClass:"ui dividing header"},[e("h2",[t._v("擷取紀錄")])])}]}},210:function(t,e){t.exports={render:function(){var t=this,e=(t.$createElement,t._c);return e("section",{staticClass:"pure-form",attrs:{id:"like"}},[t._m(0),t._v(" "),e("div",{staticClass:"pure-control-group"},[e("label",{attrs:{for:"token"}},[t._v("Token")]),t._v(" "),e("input",{directives:[{name:"model",rawName:"v-model",value:t.token,expression:"token"}],attrs:{id:"token",type:"text"},domProps:{value:t._s(t.token)},on:{input:function(e){e.target.composing||(t.token=e.target.value)}}}),t._v(" "),t._m(1)]),t._v(" "),e("table",{staticClass:"pure-table pure-table-horizontal"},[t._m(2),t._v(" "),e("tbody",t._l(t.datarows,function(a,n){return e("tr",{key:a.id,attrs:{"data-tag":a.id}},[e("td",[t._v("連結 "+t._s(n))]),t._v(" "),e("td",[e("input",{directives:[{name:"model",rawName:"v-model",value:a.url,expression:"row.url"}],attrs:{type:"text","data-id":n,id:"row"+n,name:"row"+n},domProps:{value:t._s(a.url)},on:{input:[function(t){t.target.composing||(a.url=t.target.value)},t.likesHandler]}})]),t._v(" "),e("td",[t._v(t._s(t._f("showState")(a.result.state)))]),t._v(" "),e("td",[t._v(t._s(t._f("countLength")(a.result.likes)))]),t._v(" "),e("td",[0===a.result.state?e("button",{staticClass:"pure-button pure-button-primary",attrs:{"data-id":n},on:{click:t.downloadData}},[t._v("下載")]):t._e(),t._v(" "),0===a.result.state?e("button",{staticClass:"pure-button",attrs:{"data-id":n},on:{click:t.facebookLink}},[t._v("文章連結")]):t._e(),t._v(" "),e("button",{staticClass:"pure-button",attrs:{"data-id":n},on:{click:t.deleteRow}},[t._v("刪除")])])])})),t._v(" "),e("tfoot",[e("tr",[e("td",{staticClass:"pure-controls",attrs:{colspan:"5"}},[e("button",{staticClass:"pure-button pure-button-primary",on:{click:function(t){}}},[t._v("全部送出")]),t._v(" "),e("button",{staticClass:"pure-button",on:{click:t.addRow}},[t._v("新增")])])])])])])},staticRenderFns:[function(){var t=this,e=(t.$createElement,t._c);return e("header",[e("h1",[t._v("按讚分析")])])},function(){var t=this,e=(t.$createElement,t._c);return e("span",[e("a",{attrs:{target:"_blank",href:"https://developers.facebook.com/tools/explorer/"}},[t._v("到此領取")])])},function(){var t=this,e=(t.$createElement,t._c);return e("thead",[e("tr",[e("th",[t._v("#")]),t._v(" "),e("th",[t._v("連結")]),t._v(" "),e("th",[t._v("狀態")]),t._v(" "),e("th",[t._v("按讚數")]),t._v(" "),e("th")])])}]}}});
//# sourceMappingURL=app.25de2feefb1ff1987518.js.map