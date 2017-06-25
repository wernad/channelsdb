/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var ChannelsDB;
(function (ChannelsDB) {
    'use strict';
    function readData(data) {
        return new Promise(function (resolve, reject) {
            data.onerror = function (e) {
                var error = e.target.error;
                reject(error ? error : 'Failed.');
            };
            data.onabort = function () { return reject('Aborted'); };
            data.onload = function (e) { return resolve(e); };
        });
    }
    var RequestPool = (function () {
        function RequestPool() {
        }
        RequestPool.get = function (key) {
            var ret = this.pool.length ? this.pool.pop() : new XMLHttpRequest();
            var arr = (this.pending[key || '__empty__'] || []);
            arr.push(ret);
            this.pending[key || '__empty__'] = arr;
            return ret;
        };
        RequestPool.abort = function (key) {
            var arr = this.pending[key];
            if (!arr)
                return;
            for (var _i = 0, arr_1 = arr; _i < arr_1.length; _i++) {
                var a = arr_1[_i];
                try {
                    a.abort();
                }
                catch (e) { }
            }
        };
        RequestPool.emptyFunc = function () { };
        RequestPool.removePending = function (req) {
            for (var _i = 0, _a = Object.getOwnPropertyNames(this.pending); _i < _a.length; _i++) {
                var p = _a[_i];
                var arr = this.pending[p];
                if (!arr)
                    continue;
                var idx = 0;
                for (var _b = 0, arr_2 = arr; _b < arr_2.length; _b++) {
                    var a = arr_2[_b];
                    if (a === req) {
                        arr[idx] = arr[arr.length - 1];
                        arr.pop();
                        return;
                    }
                    idx++;
                }
            }
        };
        RequestPool.deposit = function (req) {
            if (this.pool.length < this.poolSize) {
                req.onabort = RequestPool.emptyFunc;
                req.onerror = RequestPool.emptyFunc;
                req.onload = RequestPool.emptyFunc;
                req.onprogress = RequestPool.emptyFunc;
                this.removePending(req);
                this.pool.push(req);
            }
        };
        return RequestPool;
    }());
    RequestPool.pool = [];
    RequestPool.poolSize = 15;
    RequestPool.pending = {};
    ChannelsDB.RequestPool = RequestPool;
    function processAjax(e) {
        var req = e.target;
        if (req.status >= 200 && req.status < 400) {
            var text = JSON.parse(e.target.responseText);
            RequestPool.deposit(e.target);
            return text;
        }
        else {
            var status_1 = req.statusText;
            RequestPool.deposit(e.target);
            throw status_1;
        }
    }
    function ajaxGetJson(url, key) {
        return __awaiter(this, void 0, void 0, function () {
            var xhttp, e;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        xhttp = RequestPool.get(key);
                        xhttp.open('get', url, true);
                        xhttp.responseType = 'text';
                        xhttp.send();
                        return [4 /*yield*/, readData(xhttp)];
                    case 1:
                        e = _a.sent();
                        return [2 /*return*/, processAjax(e)];
                }
            });
        });
    }
    ChannelsDB.ajaxGetJson = ajaxGetJson;
})(ChannelsDB || (ChannelsDB = {}));
/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */
var ChannelsDB;
(function (ChannelsDB) {
    function updateViewState(state, viewState) {
        state.viewState = viewState;
        state.stateUpdated.onNext(void 0);
    }
    ChannelsDB.updateViewState = updateViewState;
    function initState() {
        var state = {
            dbContent: void 0,
            dbContentAvailable: new Rx.BehaviorSubject(false),
            searchedTerm: '',
            searchTerm: new Rx.Subject(),
            viewState: { kind: 'Info' },
            stateUpdated: new Rx.Subject(),
            fullSearch: new Rx.Subject(),
        };
        var interrupt = Rx.Observable.merge(state.searchTerm, state.fullSearch);
        state.searchTerm
            .do(function () { return ChannelsDB.RequestPool.abort('data'); })
            .map(function (t) { return t.trim(); })
            .distinctUntilChanged()
            .concatMap(function (t) { return Rx.Observable.timer(250).takeUntil(interrupt).map(function (_) { return t; }); })
            .forEach(function (t) {
            if (t.length > 2) {
                search(state, t).takeUntil(interrupt).subscribe(function (data) { state.searchedTerm = t; updateViewState(state, { kind: 'Searched', data: data }); }, function (err) { if (err !== 'Aborted')
                    updateViewState(state, { kind: 'Error', message: '' + err }); });
            }
            else {
                updateViewState(state, { kind: 'Info' });
            }
        });
        initSearch(state);
        return state;
    }
    ChannelsDB.initState = initState;
    function initSearch(state) {
        return __awaiter(this, void 0, void 0, function () {
            var content, e_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, ChannelsDB.ajaxGetJson('https://webchem.ncbr.muni.cz/API/ChannelsDB/Content')];
                    case 1:
                        content = _a.sent();
                        state.dbContent = { entries: content };
                        state.dbContentAvailable.onNext(true);
                        return [3 /*break*/, 3];
                    case 2:
                        e_1 = _a.sent();
                        setTimeout(function () { return initSearch(state); }, 2000);
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    function sortSearchData(state, data) {
    }
    function search(state, term) {
        ChannelsDB.RequestPool.abort('data');
        updateViewState(state, { kind: 'Loading', message: 'Searching...' });
        var s = new Rx.Subject();
        ChannelsDB.ajaxGetJson("https://www.ebi.ac.uk/pdbe/search/pdb-autocomplete/select?rows=1000000&json.nl=map&group=true&group.field=category&group.limit=28&fl=value,num_pdb_entries,var_name&sort=category+asc,num_pdb_entries+desc&q=value:" + encodeURIComponent("\"" + term + "*\"") + "~10&wt=json", 'data')
            .then(function (data) { s.onNext(data); s.onCompleted(); })
            .catch(function (err) { s.onError(err); s.onCompleted(); });
        return s;
    }
    function searchPdbCategory(term, var_name, start) {
        return __awaiter(this, void 0, void 0, function () {
            var data;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        ChannelsDB.RequestPool.abort('data');
                        return [4 /*yield*/, ChannelsDB.ajaxGetJson("https://www.ebi.ac.uk/pdbe/search/pdb-autocomplete/select?rows=28&start=" + start + "&json.nl=map&group.limit=-1&fl=value,num_pdb_entries,var_name&sort=category+asc,num_pdb_entries+desc&fq=var_name:" + var_name + "&q=value:" + encodeURIComponent("\"" + term + "*\"") + "~10&wt=json", 'data')];
                    case 1:
                        data = _a.sent();
                        return [2 /*return*/, data.response.docs];
                }
            });
        });
    }
    ChannelsDB.searchPdbCategory = searchPdbCategory;
    var ROW_COUNT = 1000000;
    var toLowerCache = {};
    function toLower(str) {
        var ret = toLowerCache[str];
        if (ret)
            return ret;
        ret = str.toLowerCase();
        toLowerCache[str] = ret;
        return ret;
    }
    ChannelsDB.toLower = toLower;
    function sortGroups(state, groups) {
        var withChannels = [], withoutChannels = [];
        var content = state.dbContent.entries;
        for (var _i = 0, groups_1 = groups; _i < groups_1.length; _i++) {
            var group = groups_1[_i];
            if (content[toLower(group.doclist.docs[0].pdb_id)])
                withChannels.push(group);
            else
                withoutChannels.push(group);
        }
        return { entries: withChannels.concat(withoutChannels), withCount: withChannels.length, withoutCount: withoutChannels.length };
    }
    function fetchPdbEntries(state, var_name, value) {
        return __awaiter(this, void 0, void 0, function () {
            var data;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, ChannelsDB.ajaxGetJson("https://www.ebi.ac.uk/pdbe/search/pdb/select?q=*:*&group=true&group.field=pdb_id&start=" + 0 + "&rows=" + ROW_COUNT + "&group.ngroups=true&fl=pdb_id,title,experimental_method,organism_scientific_name,resolution,entry_organism_scientific_name&json.nl=map&fq=" + encodeURIComponent(var_name) + ":\"" + encodeURIComponent(value) + "\"&sort=overall_quality+desc&wt=json", 'data')];
                    case 1:
                        data = _a.sent();
                        return [2 /*return*/, sortGroups(state, data.grouped.pdb_id.groups)];
                }
            });
        });
    }
    ChannelsDB.fetchPdbEntries = fetchPdbEntries;
    function fetchPdbText(state, value) {
        return __awaiter(this, void 0, void 0, function () {
            var data;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        ChannelsDB.RequestPool.abort('data');
                        return [4 /*yield*/, ChannelsDB.ajaxGetJson("https://www.ebi.ac.uk/pdbe/search/pdb/select?q=*:*&group=true&group.field=pdb_id&start=" + 0 + "&rows=" + ROW_COUNT + "&group.ngroups=true&fl=pdb_id,title,experimental_method,organism_scientific_name,resolution,entry_organism_scientific_name&json.nl=map&fq=text:\"" + encodeURIComponent(value) + "\"&sort=overall_quality+desc&wt=json", 'data')];
                    case 1:
                        data = _a.sent();
                        return [2 /*return*/, sortGroups(state, data.grouped.pdb_id.groups)];
                }
            });
        });
    }
    ChannelsDB.fetchPdbText = fetchPdbText;
})(ChannelsDB || (ChannelsDB = {}));
/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var ChannelsDB;
(function (ChannelsDB) {
    var Menu = (function (_super) {
        __extends(Menu, _super);
        function Menu() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Menu.prototype.render = function () {
            return React.createElement("nav", { className: 'navbar navbar-default' },
                React.createElement("div", { className: 'container-fluid' },
                    React.createElement("div", { className: 'navbar-header' },
                        React.createElement("a", { className: 'navbar-brand', href: 'index.html', style: { fontWeight: 'bold' } }, "ChannelsDB")),
                    React.createElement("div", { id: 'navbar', className: 'navbar-collapse collapse' },
                        React.createElement("ul", { className: 'nav navbar-nav navbar-right' },
                            React.createElement("li", null,
                                React.createElement("a", { href: 'methods.html' }, "Methods")),
                            React.createElement("li", null,
                                React.createElement("a", { href: 'documentation.html' }, "Documentation")),
                            React.createElement("li", null,
                                React.createElement("a", { href: 'http://mole.upol.cz', target: '_blank' }, "MOLE"))))));
        };
        return Menu;
    }(React.Component));
    ChannelsDB.Menu = Menu;
})(ChannelsDB || (ChannelsDB = {}));
/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */
var ChannelsDB;
(function (ChannelsDB) {
    var Intro = (function (_super) {
        __extends(Intro, _super);
        function Intro() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Intro.prototype.render = function () {
            return React.createElement("div", { style: { margin: '60px 0 0 20px', textAlign: 'justify', textJustify: 'inter-word' } },
                React.createElement("p", { className: 'lead' },
                    "ChannelsDB is a comprehensive and regulary updated resource of channels, pores and tunnels found in biomacromolecules deposited in the",
                    React.createElement("a", { target: '_blank', href: 'http://www.ebi.ac.uk/pdbe/' }, " Protein Data Bank"),
                    ". As such, it is a unique service for a channel-related analyses."),
                React.createElement("p", { className: 'text-justify' }, "The database contains information about channel positions, geometry and physicochemical properties. Additionally, all the entries are crosslinked with the UniProt database a comprehensive high-quality resource of protein function information. Last but not least, all the results are displayed in a clear interactive manner further facilitating data interpretation."),
                React.createElement("p", null,
                    "If you would like to provide your own research results to be displayed soon as a part of Protein Data Bank in Europe. ",
                    React.createElement("a", { href: 'mailto:webchemistryhelp@gmail.com' }, "Get in touch with us!"),
                    ". The application allowing for online annotation will be available later this year."));
        };
        return Intro;
    }(React.Component));
    ChannelsDB.Intro = Intro;
    var Info = (function (_super) {
        __extends(Info, _super);
        function Info() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Info.prototype.render = function () {
            var centerStyle = {
                display: 'block',
                margin: '0 auto',
                marginTop: 30,
            };
            var justify = {
                textAlign: 'justify',
                textJustify: 'inter-word',
            };
            var reference = {
                borderLeft: '2px solid #AAA',
                paddingLeft: 6,
            };
            return React.createElement("div", null,
                React.createElement("h1", { style: { marginTop: 50, textAlign: 'center' } }, "Examples"),
                React.createElement("div", { className: 'row' },
                    React.createElement("div", { className: 'col-lg-4' },
                        React.createElement("img", { style: centerStyle, className: 'img-circle', src: 'assets/img/1ymg_detail.png', alt: '1ymg channel detail', width: '140', height: '140' }),
                        React.createElement("h2", null, "Aquaporin water channel"),
                        React.createElement("p", null, "The channel architecture of Aquaporin 0 at 2.2\u212B resolution highlights residues critical for water permeation regulation."),
                        React.createElement("p", null,
                            React.createElement("a", { className: 'btn btn-default', href: '#ex-1ymg', role: 'button' }, "View details \u00BB"))),
                    React.createElement("div", { className: 'col-lg-4' },
                        React.createElement("img", { style: centerStyle, className: 'img-circle', src: 'assets/img/3tbg_detail.png', alt: '3tbg channel detail', width: '140', height: '140' }),
                        React.createElement("h2", null, "Cytochrome P450 2D6 substrate tunnel"),
                        React.createElement("p", null, "Cytochromes P450 are known for complex net of multiple channels leading towards active site. These channels serve multiple roles in substrate access, product release or hydration pathways."),
                        React.createElement("p", null,
                            React.createElement("a", { className: 'btn btn-default', href: '#ex-p450', role: 'button' }, "View details \u00BB"))),
                    React.createElement("div", { className: 'col-lg-4' },
                        React.createElement("img", { style: centerStyle, className: 'img-circle', src: 'assets/img/1jj2_detail.png', alt: '1jj2 channel detail', width: '140', height: '140' }),
                        React.createElement("h2", null, "Ribosomal polypeptide exit tunnel"),
                        React.createElement("p", null, "Ribosomal polypeptide exit tunnel directs a nascent protein from the peptidyl transferase center to the outside of the ribosome."),
                        React.createElement("p", null,
                            React.createElement("a", { className: 'btn btn-default', href: '#ex-1jj2', role: 'button' }, "View details \u00BB")))),
                React.createElement("hr", { className: 'featurette-divider', style: { margin: '50px 0' } }),
                React.createElement("div", { className: 'row featurette' },
                    React.createElement("a", { name: 'ex-1ymg' }),
                    React.createElement("div", { className: 'col-md-7' },
                        React.createElement("a", { href: 'http://channelsdb.dominiktousek.eu/ChannelsDB/detail/1ymg' },
                            React.createElement("h2", { className: 'featurette-heading' },
                                "Aquaporin O ",
                                React.createElement("span", { className: 'text-muted' }, "(1ymg)"))),
                        React.createElement("p", { className: 'lead' }, "The channel architecture of Aquaporin O at 2.2\u212B resolution highlights residues critical for water permeation regulation."),
                        React.createElement("p", { style: justify }, "The channel is ~ 30\u212B long and highlights with some of the residues crucial for its proper function. Selectivity filter (ar/R), which allows water molecules passage through the membrane in a single file (green sticks). Residues providing canonical AQP hydrogen bond acceptor that align watters through the channel in balls and stick model. Finally, Tyr-149 important for channel gating in orange."),
                        React.createElement("p", { style: reference },
                            React.createElement("small", null,
                                React.createElement("a", { target: '_blank', href: 'https://dx.doi.org/10.1073/pnas.0405274101' },
                                    "Harries, W. E. C., et. al. ",
                                    React.createElement("span", { style: { fontStyle: 'italic' } }, "The channel architecture of aquaporin 0 at a 2.2\u212B resolution"),
                                    ". Proc. Natl. Acad. Sci. 101, 14045\u201314050 (2004)")))),
                    React.createElement("div", { className: 'col-md-5' },
                        React.createElement("img", { className: 'featurette-image img-responsive center-block', src: 'assets/img/1ymg.png', width: '500', height: '500', alt: '1ymg detailed channel view' }))),
                React.createElement("hr", { className: 'featurette-divider', style: { margin: '50px 0' } }),
                React.createElement("div", { className: 'row featurette' },
                    React.createElement("a", { name: 'ex-p450' }),
                    React.createElement("div", { className: 'col-md-7 col-md-push-5' },
                        React.createElement("a", { href: 'http://channelsdb.dominiktousek.eu/ChannelsDB/detail/3tbg' },
                            React.createElement("h2", { className: 'featurette-heading' },
                                "Cytochrome P450 2D6 ",
                                React.createElement("span", { className: 'text-muted' }, "(3tbg)"))),
                        React.createElement("p", { className: 'lead' }, "Cytochromes P450 are known for complex net of multiple channels leading towards active site. These channels serve multiple roles in substrate access, product release or hydration pathways."),
                        React.createElement("p", { style: justify },
                            "Cytochrome  P450  2D6  contributes  significantly  to  the  metabolism  of  >15%  of  the  200  most marketed drugs. Cytochrome P450 2D6 structure shows a second molecule of thioridazine bound in an expanded substrate access channel (channel  2a according to Cojocaru et  al. ",
                            React.createElement("a", { href: 'https://doi.org/10.1016/j.bbagen.2006.07.005', target: '_blank' }, "classification"),
                            "  antechamber  with  its  piperidine  moiety  forming  a charge-stabilized hydrogen bond with Glu-222."),
                        React.createElement("p", { style: reference },
                            React.createElement("small", null,
                                React.createElement("a", { target: '_blank', href: 'https://dx.doi.org/10.1074/jbc.M114.627661' },
                                    "Wang, A., et al. ",
                                    React.createElement("span", { style: { fontStyle: 'italic' } }, "Contributions of Ionic Interactions and Protein Dynamics to Cytochrome P450 2D6 (CYP2D6) Substrate and Inhibitor Binding"),
                                    " J.Biol.Chem. 290: 5092-5104 (2015)")))),
                    React.createElement("div", { className: 'col-md-5 col-md-pull-7' },
                        React.createElement("img", { className: 'featurette-image img-responsive center-block', src: 'assets/img/3tbg.png', alt: 'Cytochrome P450 substrate channel details' }))),
                React.createElement("hr", { className: 'featurette-divider', style: { margin: '50px 0' } }),
                React.createElement("div", { className: 'row featurette' },
                    React.createElement("a", { name: 'ex-1jj2' }),
                    React.createElement("div", { className: 'col-md-7 ' },
                        React.createElement("a", { href: 'http://channelsdb.dominiktousek.eu/ChannelsDB/detail/1jj2' },
                            React.createElement("h2", { className: 'featurette-heading' },
                                "Large Ribosomal Subunit ",
                                React.createElement("span", { className: 'text-muted' }, "(1jj2)"))),
                        React.createElement("p", { className: 'lead' }, "The ribosomal polypeptide tunnel provides an insight into the release of a nascent polypeptide chain out of the ribosomal complex."),
                        React.createElement("p", { style: justify }, "The exit tunnel is surrounded by arginine side chains (stick model), bearing positive charges as well as RNA backbone phosphate groups (spheres), thus providing fragmental charge along the tunnel, which is necessary to prevent the nasccent peptide from sticking to the channel wall inside the ribosome. Subunits L4, L22 and L39e interacting with the exit tunnel are highlighted in yellow, green and magenta respectivelly."),
                        React.createElement("p", { style: reference },
                            React.createElement("small", null,
                                React.createElement("a", { target: '_blank', href: 'https://dx.doi.org/10.1016/j.jmb.2006.05.023' },
                                    "Voss, N. R., et. al. ",
                                    React.createElement("span", { style: { fontStyle: 'italic' } }, "The geometry of the ribosomal polypeptide exit tunnel."),
                                    ". J. Mol. Biol. 360, 893\u2013906 (2006)")))),
                    React.createElement("div", { className: 'col-md-5 ' },
                        React.createElement("img", { className: 'featurette-image img-responsive center-block', src: 'assets/img/1jj2.png', alt: 'Polypeptide exit tunnel' }))));
        };
        return Info;
    }(React.Component));
    ChannelsDB.Info = Info;
})(ChannelsDB || (ChannelsDB = {}));
/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */
var ChannelsDB;
(function (ChannelsDB) {
    var Methods = (function (_super) {
        __extends(Methods, _super);
        function Methods() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Methods.prototype.render = function () {
            var justify = {
                textAlign: 'justify',
                textJustify: 'inter-word',
            };
            var reference = {
                borderLeft: '2px solid #AAA',
                paddingLeft: 6,
            };
            return React.createElement("div", { style: { margin: '60px 0 0 20px' } },
                React.createElement("div", { className: 'row' },
                    React.createElement("div", { className: 'col-md-7' },
                        React.createElement("h2", { className: 'featurette-heading' }, "Channels"),
                        React.createElement("p", { style: justify }, "Channels and pores are important regions of proteins and other biomacromolecules. They connect internal spaces of biomacromolecules with exterior enabling, e.g., substrates/product transport towards enzymes\u2019 active sites, nascent synthetized proteins to leave ribosomal proteosynthetic center via ribosomal exit channel, etc. Pores represent a pathway passing through the whole biomacromolecular structure, typically facilitating transport of ions or molecules through cellular biomembranes."),
                        React.createElement("p", { style: justify },
                            "Channel walls are made from surrounding amino acids making up for a ",
                            React.createElement("a", { href: 'http://dx.doi.org/10.1186/s12859-014-0379-x', target: '_blank' }, "specific micro-environment"),
                            ", which influence to a great extent specificity and selectivity of plethora biologically important processes. Their constitution is especially important in channel's constriction sites such as local minimas and bottlenecks, which can function as gatekeepers."),
                        React.createElement("p", { style: justify }, "In the database a channel is represented by its centerline and a radius towards the closest protein atom. All the channel lining residues are reported altogether with the physicochemical properties.")),
                    React.createElement("div", { className: 'col-md-5' },
                        React.createElement("img", { className: 'featurette-image img-responsive center-block', src: 'assets/img/channel_detail.png', width: '500', height: '500', alt: 'Channel details' }))),
                React.createElement("hr", { className: 'featurette-divider', style: { margin: '50px 0' } }),
                React.createElement("div", { className: 'row featurette' },
                    React.createElement("h2", { className: 'featurette-heading' }, "MOLE"),
                    React.createElement("div", { className: 'col-md-7 col-md-push-5' },
                        React.createElement("p", null, "MOLE is a software tool used for channel identification throughout the database. First, the algorithm calculates Delaunay triangulation/Voronoi diagram of the atomic centers (1). Next, regions suitable for channel indentification are calculated using a set of predefined parameters (2,3). Channel starting and end poinst are identified on these cavity diagrams (4,5) and the most favourable channels are identified among a set of point end points (6)."),
                        React.createElement("p", null,
                            "Once the channels have been identified a unique set of residues surrounding channel volume is retrieved. Given this set of residues, a physicochemical properties such as Hydropathy are computed for each channel and its parts. Individual steps of the algorithm are highlighted at the picture below  and more details on the channel identification can be found in the respective ",
                            React.createElement("a", { href: 'http://dx.doi.org/10.1186/1758-2946-5-39', target: '_blank' }, "paper"),
                            ". Finally, user structures can be analysed using the ",
                            React.createElement("a", { href: 'http://mole.upol.cz', target: '_blank' }, "online"),
                            " as well as with the ",
                            React.createElement("a", { href: 'https://webchem.ncbr.muni.cz/Platform/App/Mole', target: '_blank' }, "command-line"),
                            " version of MOLE.")),
                    React.createElement("div", { className: 'col-md-5 col-md-pull-7' },
                        React.createElement("img", { className: 'featurette-image img-responsive center-block', src: 'assets/img/alg_outline.jpg', width: '500', height: '500', alt: 'Channel details' }))),
                React.createElement("hr", { className: 'featurette-divider', style: { margin: '50px 0' } }),
                React.createElement("div", { className: 'row' },
                    React.createElement("div", { className: 'col-md-12' },
                        React.createElement("h2", { className: 'featurette-heading' }, "Physicochemical properties"),
                        React.createElement("p", null, "Altogether with the position and radius of a channel a set of unique residues constituting the channel walls is reported. This set is in turn used for estimation of a various chemicophysical properties."),
                        React.createElement("div", { className: 'col-md-6' },
                            React.createElement("h2", { className: 'featurette-heading' }, "Hydropathy"),
                            React.createElement("p", { style: justify }, "Hydrophobicity and hydrophilicity are two extremes of a spectrum, commonly referred to as Hydropathy, and relate to the tendency of a molecule to interact with water. Several hydropathy scales have been developed in order to grasp the overall character of proteins or their parts. Kyte-Doolittle scale is a widely applied measure for expressing the hydrophobicity of amino acids residues. Regions with values above 0 are considered hydrophobic in character."),
                            React.createElement("p", null, "The scale is symethrical in interval from -4.5 (Arg) to 4.5 (Ile)."),
                            React.createElement("p", { style: reference },
                                React.createElement("small", null,
                                    React.createElement("a", { target: '_blank', href: 'https://dx.doi.org/10.1016/0022-2836(82)90515-0' },
                                        "Kyte, J. & Doolittle, R. F. ",
                                        React.createElement("span", { style: { fontStyle: 'italic' } }, "A simple method for displaying the hydropathic character of a protein."),
                                        "J. Mol. Biol. 157, 105\u2013132 (1982)")))),
                        React.createElement("div", { className: 'col-md-6' },
                            React.createElement("h2", { className: 'featurette-heading' }, "Polarity"),
                            React.createElement("p", { style: justify }, "Polarity is the property of a molecule given by the separation of electric charge, leading to the molecule having electric poles. Generally speaking, polar molecules are hydrophilic, while non polar molecules are usually hydrophobic, but there can be exceptions. In the terms of amino acids residues, hydrophilic/polar and hydrophobic/non polar can be considered as synonyms."),
                            React.createElement("p", null, "The scale ranges from 0 for small aliphatic amino acids (Ala, Gly) to 51.6 (His)."),
                            React.createElement("p", { style: reference },
                                React.createElement("small", null,
                                    React.createElement("a", { target: '_blank', href: 'https://dx.doi.org/10.1016/0022-5193(68)90069-6' },
                                        "Zimmerman, J. M., Eliezer, N. &amph; Simha, R ",
                                        React.createElement("span", { style: { fontStyle: 'italic' } }, "The characterization of amino acid sequences in proteins by statistical methods."),
                                        "J. Theor. Biol. 21, 170\u2013201 (1968).")))))),
                React.createElement("div", { className: 'row' },
                    React.createElement("div", { className: 'col-md-6' },
                        React.createElement("h2", { className: 'featurette-heading' }, "Mutability"),
                        React.createElement("p", { style: justify }, "Relative mutability quantifies the tendency of an amino acid to be substituted (mutated) in a protein structure. Substitution by similar amino acids generally retains protein function, while substitution by amino acids with different properties may affect the protein structure or function. Relative mutability is high for easily substitutable amino acids, such as small polar residues and low for amino acids which play a significant role in protein structure, i.e. substrate binding or catalytic activity. Alanine has a normalized value of 100."),
                        React.createElement("p", { style: reference },
                            React.createElement("small", null,
                                React.createElement("a", { target: '_blank', href: 'https://dx.doi.org/10.1093/bioinformatics/8.3.275' },
                                    "Jones, D. T., Taylor, W. R. &amph; Thornton, J. M. ",
                                    React.createElement("span", { style: { fontStyle: 'italic' } }, "The rapid generation of mutation data matrices from protein sequences."),
                                    "Bioinformatics 8, 275\u2013282 (1992)")))),
                    React.createElement("div", { className: 'col-md-6' },
                        React.createElement("h2", { className: 'featurette-heading' }, "Charge"),
                        React.createElement("p", { style: justify }, "Some amino acids can be (de)protonated based on the pH and, therefore, charged. At physiological pH, lysine and arginine are positively charged, whereas aspartic and glutamic acids are negatively charged. On the other hand, the protonation state of histidine is dependent on its micro-environment. In this study, all histidines are treated as positively charged."),
                        React.createElement("p", null, "Charge property is a sum of all positively and negatively charged amino acids.")),
                    React.createElement("div", { style: { marginTop: 30 }, className: 'row table-responsive col-md-8 col-md-offset-2' },
                        React.createElement("table", { className: 'table table-condensed active' },
                            React.createElement("thead", null,
                                React.createElement("tr", null,
                                    React.createElement("th", null, "Residue"),
                                    React.createElement("th", null, "Charge"),
                                    React.createElement("th", null, "Hydrpathy"),
                                    React.createElement("th", null, "Polarity"),
                                    React.createElement("th", null, "Mutability"))),
                            React.createElement("tbody", null,
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Ala"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "1.8"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "100")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Arg"),
                                    React.createElement("td", null, "1"),
                                    React.createElement("td", null, "-4.5"),
                                    React.createElement("td", null, "52"),
                                    React.createElement("td", null, "83")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Asn"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "-3.5"),
                                    React.createElement("td", null, "3.38"),
                                    React.createElement("td", null, "104")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Asp"),
                                    React.createElement("td", null, "-1"),
                                    React.createElement("td", null, "-3.5"),
                                    React.createElement("td", null, "49.7"),
                                    React.createElement("td", null, "86")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Cys"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "2.5"),
                                    React.createElement("td", null, "1.48"),
                                    React.createElement("td", null, "44")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Glu"),
                                    React.createElement("td", null, "-1"),
                                    React.createElement("td", null, "-3.5"),
                                    React.createElement("td", null, "49.9"),
                                    React.createElement("td", null, "77")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Gln"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "-3.5"),
                                    React.createElement("td", null, "3.53"),
                                    React.createElement("td", null, "84")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Gly"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "-0.4"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "50")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "His"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "-3.2"),
                                    React.createElement("td", null, "51.6"),
                                    React.createElement("td", null, "91")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Ile"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "4.5"),
                                    React.createElement("td", null, "0.13"),
                                    React.createElement("td", null, "103")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Leu"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "3.8"),
                                    React.createElement("td", null, "0.13"),
                                    React.createElement("td", null, "54")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Lys"),
                                    React.createElement("td", null, "1"),
                                    React.createElement("td", null, "-3.9"),
                                    React.createElement("td", null, "49.5"),
                                    React.createElement("td", null, "72")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Met"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "1.9"),
                                    React.createElement("td", null, "1.43"),
                                    React.createElement("td", null, "93")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Phe"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "2.8"),
                                    React.createElement("td", null, "0.35"),
                                    React.createElement("td", null, "51")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Pro"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "-1.6"),
                                    React.createElement("td", null, "1.58"),
                                    React.createElement("td", null, "58")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Ser"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "-0.8"),
                                    React.createElement("td", null, "1.67"),
                                    React.createElement("td", null, "117")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Thr"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "-0.7"),
                                    React.createElement("td", null, "1.66"),
                                    React.createElement("td", null, "107")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Trp"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "-0.9"),
                                    React.createElement("td", null, "2.1"),
                                    React.createElement("td", null, "25")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Tyr"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "-1.3"),
                                    React.createElement("td", null, "1.61"),
                                    React.createElement("td", null, "50")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Val"),
                                    React.createElement("td", null, "0"),
                                    React.createElement("td", null, "4.2"),
                                    React.createElement("td", null, "0.13"),
                                    React.createElement("td", null, "98")))))));
        };
        return Methods;
    }(React.Component));
    ChannelsDB.Methods = Methods;
})(ChannelsDB || (ChannelsDB = {}));
/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */
var ChannelsDB;
(function (ChannelsDB) {
    var Documentation = (function (_super) {
        __extends(Documentation, _super);
        function Documentation() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Documentation.prototype.render = function () {
            var justify = {
                textAlign: 'justify',
                textJustify: 'inter-word',
            };
            return React.createElement("div", { style: { margin: '60px 0 0 20px' } },
                React.createElement("h1", { className: 'text-center' }, "Documentation"),
                React.createElement("div", { className: 'row' },
                    React.createElement("div", { className: 'col-md-8' },
                        React.createElement("h2", { className: 'featurette-heading' }, "Database content"),
                        React.createElement("p", null,
                            React.createElement("b", null, "The entire database is composed out of the following content:"),
                            React.createElement("ul", null,
                                React.createElement("li", null, "Hand currated channel annotations from literature extracted entries"),
                                React.createElement("li", null,
                                    "Ligad-accessible tunnels to the catalytic sites annotated in the ",
                                    React.createElement("a", { target: '_blank', href: 'http://www.ebi.ac.uk/thornton-srv/databases/CSA/' }, "Catalytic Site Atlas")),
                                React.createElement("li", null,
                                    "Pores in transmembrane proteins enabling flow of ions and small molecules across the lipid bilayer for proteins deposited in the ",
                                    React.createElement("a", { target: '_blank', href: 'http://opm.phar.umich.edu/' }, "OPM"),
                                    " database"),
                                React.createElement("li", null,
                                    "Product/substrate tunnels leading towards the well-known enzyme cofactors such as ",
                                    React.createElement("abbr", { className: 'abbr initialism', title: 'HEME (Protoporhpyrin IX containing Fe)' }, "HEM"),
                                    " or ",
                                    React.createElement("abbr", { className: 'abbr initialism', title: 'Flavin-adenine dinucleotide' }, "FAD"))),
                            "All the channels have been extracted from biological assemblies as identified by the Protein Data Bank in Europe.")),
                    React.createElement("div", { className: 'col-md-4' },
                        React.createElement("img", { className: 'featurette-image img-responsive center-block', src: 'assets/img/pretty_channel.png', width: '500', height: '500', alt: 'Channel details' }))),
                React.createElement("hr", { className: 'featurette-divider', style: { margin: '50px 0' } }),
                React.createElement("div", { className: 'row' },
                    React.createElement("h2", { className: 'featurette-heading' }, "Channel nomenclature"),
                    React.createElement("p", null,
                        "Unless the channel has been given a particular name in literature, which is the case e.g. for a group of ",
                        React.createElement("a", { href: 'https://dx/doi.org/10.1016/j.bbagen.2006.07.005', target: '_blank' }, "cytorchome P450s"),
                        ", names are given to according to the following controlled vocabulary:"),
                    React.createElement("div", { className: 'row table-responsive col-md-8 col-md-offset-2' },
                        React.createElement("table", { className: 'table table-condensed active' },
                            React.createElement("thead", null,
                                React.createElement("tr", null,
                                    React.createElement("th", null, "Name"),
                                    React.createElement("th", null, "Description"))),
                            React.createElement("tbody", null,
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Channel"),
                                    React.createElement("td", null, "Generic term for any ligand transporting pathway")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Tunnel"),
                                    React.createElement("td", null, "Generic term for a ligand transporting pathway towards the enzyme active site")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Pore"),
                                    React.createElement("td", null, "Generic term for a channel spanning across a lipid bilayer")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Solvent channel"),
                                    React.createElement("td", null, "Channel transporting water molecules, which are consumed/egressed during a chemical reaction")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Water channel"),
                                    React.createElement("td", null, "Transports water molecules; mainly found in aquaporins.")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Substrate tunnel"),
                                    React.createElement("td", null, "Channel transporting various chemical species consumed in a chemical reaction")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Product tunnel"),
                                    React.createElement("td", null, "Transports chemical species that are an outcome of chemical reaction")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Ion channel"),
                                    React.createElement("td", null, "Provides pathways for ion and other charged chemical species to pass through lipid bilayer")),
                                React.createElement("tr", null,
                                    React.createElement("td", null, "Hydrophobic channel"),
                                    React.createElement("td", null, "Provides pathways for apolar chemical species to pass through lipid bilayer")))))),
                React.createElement("hr", { className: 'featurette-divider', style: { margin: '50px 0' } }),
                React.createElement("div", { className: 'row featurette' },
                    React.createElement("h2", { className: 'featurette-heading' }, "Results interpretation"),
                    React.createElement("div", { className: 'col-md-5' },
                        React.createElement("p", { style: justify }, "The results page is separated into 5 different sections. All of them are interactive, so play around!"),
                        React.createElement("ol", null,
                            React.createElement("li", null,
                                "The main part contains molecule visualization using LiteMol. The documentation how to change visual representation of the results is available in the ",
                                React.createElement("a", { href: 'https://webchem.ncbr.muni.cz/Wiki/LiteMol:UserManual', target: '_blank' }, "LiteMol documentation"),
                                "."),
                            React.createElement("li", null, "Right next to the visualization pane a list of all channels identified for the particular PDB entry is displayed. Channels are grouped to the respective categories"),
                            React.createElement("li", null, "Directly below the visualization pane you can fin an interactive visualilization of a channel profile. All the physicochemical properties are mapped on the channel profile, so the user can select deemed type of visualization. Export to a publication quality image is available as well."),
                            React.createElement("li", null, "Next to the 2D channel visualization is a panel with details for individual regions of the channel so called layers. Additional level of information is provided as a residue level annotations with respective reference."),
                            React.createElement("li", null, " Protein annotatio from the UniProt resource"))),
                    React.createElement("div", { className: 'col-md-7' },
                        React.createElement("img", { className: 'featurette-image img-responsive center-block', src: 'assets/img/web-fig1.png', width: '500', height: '500', alt: 'Result window detail' }))),
                React.createElement("div", { style: { margin: '50px 0' }, className: 'row featurette col-md-12' },
                    React.createElement("img", { className: 'featurette-image img-responsive center-block', src: 'assets/img/web-fig2.png', width: '800', alt: '2D detailed channel view' })));
        };
        return Documentation;
    }(React.Component));
    ChannelsDB.Documentation = Documentation;
})(ChannelsDB || (ChannelsDB = {}));
/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
var ChannelsDB;
(function (ChannelsDB) {
    function renderUI(target, kind) {
        switch (kind) {
            case 'Search':
                ReactDOM.render(React.createElement(SearchMain, { state: ChannelsDB.initState() }), target);
                break;
            case 'Methods':
                ReactDOM.render(React.createElement(MethodsMain, null), target);
                break;
            case 'Documentation':
                ReactDOM.render(React.createElement(DocumentationMain, null), target);
                break;
        }
    }
    ChannelsDB.renderUI = renderUI;
    var SearchMain = (function (_super) {
        __extends(SearchMain, _super);
        function SearchMain() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        SearchMain.prototype.render = function () {
            return React.createElement("div", { className: 'container' },
                React.createElement(ChannelsDB.Menu, null),
                React.createElement(ChannelsDB.Intro, null),
                React.createElement(SearchView, __assign({}, this.props)),
                React.createElement(Footer, null));
        };
        return SearchMain;
    }(React.Component));
    var MethodsMain = (function (_super) {
        __extends(MethodsMain, _super);
        function MethodsMain() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        MethodsMain.prototype.render = function () {
            return React.createElement("div", { className: 'container' },
                React.createElement(ChannelsDB.Menu, null),
                React.createElement(ChannelsDB.Methods, null),
                React.createElement(Footer, null));
        };
        return MethodsMain;
    }(React.Component));
    var DocumentationMain = (function (_super) {
        __extends(DocumentationMain, _super);
        function DocumentationMain() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        DocumentationMain.prototype.render = function () {
            return React.createElement("div", { className: 'container' },
                React.createElement(ChannelsDB.Menu, null),
                React.createElement(ChannelsDB.Documentation, null),
                React.createElement(Footer, null));
        };
        return DocumentationMain;
    }(React.Component));
    var Footer = (function (_super) {
        __extends(Footer, _super);
        function Footer() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Footer.prototype.render = function () {
            return React.createElement("footer", null,
                React.createElement("hr", { className: 'featurette-divider' }),
                React.createElement("p", { className: 'pull-right', style: { color: '#999', fontSize: 'smaller', marginBottom: '30px' } }, "\u00A9 2017 Luk\u00E1\u0161 Pravda & David Sehnal"));
        };
        return Footer;
    }(React.Component));
    var SearchView = (function (_super) {
        __extends(SearchView, _super);
        function SearchView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        SearchView.prototype.render = function () {
            return React.createElement("div", { style: { marginTop: '35px' } },
                React.createElement("div", { className: 'row' },
                    React.createElement("div", { className: 'col-lg-12' },
                        React.createElement(SearchBox, __assign({}, this.props)))),
                React.createElement("div", { className: 'row' },
                    React.createElement("div", { className: 'col-lg-12' },
                        React.createElement(StateView, __assign({}, this.props)))));
        };
        return SearchView;
    }(React.Component));
    var StateView = (function (_super) {
        __extends(StateView, _super);
        function StateView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        StateView.prototype.componentDidMount = function () {
            var _this = this;
            this.props.state.stateUpdated.subscribe(function () { return _this.forceUpdate(); });
        };
        StateView.prototype.render = function () {
            var state = this.props.state.viewState;
            try {
                switch (state.kind) {
                    case 'Info': return React.createElement(ChannelsDB.Info, null);
                    case 'Loading': return React.createElement("div", null, state.message);
                    case 'Searched': return React.createElement(SearchResults, __assign({}, this.props));
                    case 'Entries': return React.createElement(Entries, __assign({}, this.props, { mode: 'Full', value: state.term }));
                    case 'Error': return React.createElement("div", null,
                        "Error: ",
                        state.message);
                    default: return React.createElement("div", null, "Should not happen ;)");
                }
            }
            catch (e) {
                return React.createElement("div", null,
                    "Error: ",
                    '' + e);
            }
        };
        return StateView;
    }(React.Component));
    var SearchBox = (function (_super) {
        __extends(SearchBox, _super);
        function SearchBox() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { isAvailable: false };
            return _this;
        }
        SearchBox.prototype.componentDidMount = function () {
            var _this = this;
            this.props.state.dbContentAvailable.subscribe(function (isAvailable) { return _this.setState({ isAvailable: isAvailable }); });
        };
        SearchBox.prototype.render = function () {
            var _this = this;
            return React.createElement("div", { className: 'form-group form-group-lg' }, this.state.isAvailable
                ? React.createElement("input", { key: 'fullsearch', type: 'text', className: 'form-control', style: { fontWeight: 'bold' }, placeholder: 'Search ChannelsDB (e.g., cytochrome p450, 5an8, KcsA) ...', onChange: function (e) { return _this.props.state.searchTerm.onNext(e.target.value); }, onKeyPress: function (e) {
                        if (e.key !== 'Enter')
                            return;
                        _this.props.state.fullSearch.onNext(void 0);
                        ChannelsDB.updateViewState(_this.props.state, { kind: 'Entries', term: e.target.value });
                    } })
                : React.createElement("input", { key: 'placeholder', type: 'text', className: 'form-control', style: { fontWeight: 'bold', textAlign: 'center' }, disabled: true, value: 'Initializing search...' }));
        };
        return SearchBox;
    }(React.Component));
    var SearchResults = (function (_super) {
        __extends(SearchResults, _super);
        function SearchResults() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        SearchResults.prototype.empty = function () {
            return React.createElement("div", null, "No results");
        };
        SearchResults.prototype.groups = function () {
            var _this = this;
            var data = this.props.state.viewState.data;
            var groups = data.grouped.category.groups;
            return groups.map(function (g, i) { return React.createElement(SearchGroup, __assign({ key: g.groupValue + '--' + i }, _this.props, { group: g })); });
        };
        SearchResults.prototype.render = function () {
            try {
                var data = this.props.state.viewState.data;
                if (!data.grouped.category.groups.length)
                    return this.empty();
                return React.createElement("div", null,
                    React.createElement("div", { style: { padding: '0 0 15px 0', marginTop: '-15px', fontStyle: 'italic', textAlign: 'right' } },
                        React.createElement("small", null, "Press 'Enter' for full-text search.")),
                    React.createElement("div", null, this.groups()));
            }
            catch (e) {
                return this.empty();
            }
        };
        return SearchResults;
    }(React.Component));
    var SearchGroup = (function (_super) {
        __extends(SearchGroup, _super);
        function SearchGroup() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { isExpanded: false, docs: [], isLoading: false, entries: void 0 };
            _this.toggle = function (e) {
                e.preventDefault();
                _this.setState({ isExpanded: !_this.state.isExpanded });
            };
            _this.showEntries = function (e) {
                e.preventDefault();
                var value = e.target.getAttribute('data-value');
                var var_name = e.target.getAttribute('data-var');
                var count = +e.target.getAttribute('data-count');
                _this.setState({ entries: { group: _this.props.group.groupValue, value: value, var_name: var_name, count: count } });
            };
            _this.loadMore = function () { return __awaiter(_this, void 0, void 0, function () {
                var docs, e_2;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, , 3]);
                            this.setState({ isLoading: true });
                            return [4 /*yield*/, ChannelsDB.searchPdbCategory(this.props.state.searchedTerm, this.state.docs[0].var_name, this.state.docs.length)];
                        case 1:
                            docs = _a.sent();
                            this.setState({ isLoading: false, docs: this.state.docs.concat(docs) });
                            return [3 /*break*/, 3];
                        case 2:
                            e_2 = _a.sent();
                            this.setState({ isLoading: false });
                            return [3 /*break*/, 3];
                        case 3: return [2 /*return*/];
                    }
                });
            }); };
            return _this;
        }
        SearchGroup.prototype.componentDidMount = function () {
            this.setState({ docs: this.props.group.doclist.docs });
        };
        SearchGroup.prototype.entry = function (d, i) {
            return React.createElement("div", { key: d.value + d.var_name + '--' + i },
                React.createElement("a", { href: '#', "data-value": d.value, "data-var": d.var_name, "data-count": d.num_pdb_entries, onClick: this.showEntries, title: "" + d.value }, d.value),
                React.createElement("div", { className: 'count' }, d.num_pdb_entries));
        };
        SearchGroup.prototype.render = function () {
            var _this = this;
            var g = this.props.group;
            return React.createElement("div", { style: { marginBottom: '10px' } },
                React.createElement("div", { className: 'group-header' },
                    React.createElement("button", { className: 'btn btn-default btn-block', onClick: this.toggle },
                        React.createElement("span", { className: "glyphicon glyphicon-" + (this.state.isExpanded ? 'minus' : 'plus'), "aria-hidden": 'true' }),
                        " ",
                        React.createElement("span", null, g.groupValue),
                        " (",
                        g.doclist.numFound,
                        ")")),
                React.createElement("div", { className: 'group-list-wrap', style: { display: this.state.entries ? 'none' : 'block' } },
                    React.createElement("div", { className: 'group-list', style: { display: this.state.isExpanded ? 'block' : 'none' } },
                        this.state.docs.map(function (d, i) { return _this.entry(d, i); }),
                        this.state.docs.length < g.doclist.numFound
                            ? React.createElement("div", { style: { padding: 0, float: 'none', clear: 'both' } },
                                React.createElement("button", { style: { width: '100%', display: 'block' }, className: 'btn btn-xs btn-primary btn-block', disabled: this.state.isLoading ? true : false, onClick: this.loadMore }, this.state.isLoading ? 'Loading...' : "More (" + (g.doclist.numFound - this.state.docs.length) + " remaining)"))
                            : void 0),
                    React.createElement("div", { style: { clear: 'both' } })),
                this.state.entries && this.state.isExpanded
                    ? React.createElement("div", { className: 'entry-list-wrap' },
                        React.createElement("button", { className: 'btn btn-block btn-primary', onClick: function () { return _this.setState({ entries: void 0 }); } },
                            React.createElement("span", { className: "glyphicon glyphicon-chevron-left", "aria-hidden": 'true' })),
                        React.createElement(Entries, __assign({ state: this.props.state }, this.state.entries, { mode: 'Embed' })))
                    : void 0);
        };
        return SearchGroup;
    }(React.Component));
    var Entry = (function (_super) {
        __extends(Entry, _super);
        function Entry() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Entry.prototype.render = function () {
            var docs = this.props.docs;
            var entry = this.props.state.dbContent.entries[ChannelsDB.toLower(docs.pdb_id)];
            var numChannels = entry ? entry.counts.reduce(function (a, b) { return a + b; }, 0) : -1;
            return React.createElement("div", { className: 'well pdb-entry' },
                React.createElement("a", { href: "http://channelsdb.dominiktousek.eu/ChannelsDB/detail/" + docs.pdb_id, target: '_blank' },
                    React.createElement("div", { className: 'pdb-entry-header', style: { background: entry ? '#dfd' : '#ddd' } },
                        React.createElement("div", null, docs.pdb_id),
                        React.createElement("div", { title: docs.title || 'n/a' }, docs.title || 'n/a'))),
                React.createElement("ul", null,
                    React.createElement("li", null,
                        React.createElement("b", null, "Experiment Method:"),
                        " ",
                        (docs.experimental_method || ['n/a']).join(', '),
                        " | ",
                        docs.resolution || 'n/a',
                        " \u00C5"),
                    React.createElement("li", null,
                        React.createElement("b", null, "Organism:"),
                        " ",
                        React.createElement("i", null, (docs.organism_scientific_name || ['n/a']).join(', '))),
                    numChannels > 0
                        ? React.createElement("li", null,
                            React.createElement("i", null, numChannels + " channel" + (numChannels !== 1 ? 's' : '') + " (" + entry.counts.length + " computation" + (entry.counts.length !== 1 ? 's' : '') + ")"))
                        : void 0),
                React.createElement("div", { className: 'pdb-entry-img-wrap' },
                    React.createElement("img", { src: "https://webchem.ncbr.muni.cz/API/ChannelsDB/Download/" + docs.pdb_id.toLowerCase() + "?type=figure" })));
        };
        return Entry;
    }(React.Component));
    var Entries = (function (_super) {
        __extends(Entries, _super);
        function Entries() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { isLoading: false, entries: [], count: -1, showing: 0, withCount: -1, withoutCount: -1 };
            _this.fetchEmbed = function () { return __awaiter(_this, void 0, void 0, function () {
                var _a, entries, withCount, withoutCount, e_3;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            _c.trys.push([0, 2, , 3]);
                            this.setState({ isLoading: true });
                            return [4 /*yield*/, ChannelsDB.fetchPdbEntries(this.props.state, this.props.var_name, this.props.value)];
                        case 1:
                            _a = _c.sent(), entries = _a.entries, withCount = _a.withCount, withoutCount = _a.withoutCount;
                            this.setState({ isLoading: false, entries: entries, count: withCount + withoutCount, withCount: withCount, withoutCount: withoutCount, showing: this.growFactor });
                            return [3 /*break*/, 3];
                        case 2:
                            e_3 = _c.sent();
                            this.setState({ isLoading: false });
                            return [3 /*break*/, 3];
                        case 3: return [2 /*return*/];
                    }
                });
            }); };
            _this.fetchFull = function () { return __awaiter(_this, void 0, void 0, function () {
                var _a, entries, withCount, withoutCount, e_4;
                return __generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            _c.trys.push([0, 2, , 3]);
                            this.setState({ isLoading: true });
                            return [4 /*yield*/, ChannelsDB.fetchPdbText(this.props.state, this.props.value)];
                        case 1:
                            _a = _c.sent(), entries = _a.entries, withCount = _a.withCount, withoutCount = _a.withoutCount;
                            this.setState({ isLoading: false, entries: entries, count: withCount + withoutCount, withCount: withCount, withoutCount: withoutCount, showing: this.growFactor });
                            return [3 /*break*/, 3];
                        case 2:
                            e_4 = _c.sent();
                            this.setState({ isLoading: false });
                            return [3 /*break*/, 3];
                        case 3: return [2 /*return*/];
                    }
                });
            }); };
            _this.loadMore = function () { return _this.setState({ showing: _this.state.showing + _this.growFactor }); };
            _this.growFactor = _this.props.mode === 'Embed' ? 6 : 12;
            _this.fetch = _this.props.mode === 'Embed' ? _this.fetchEmbed : _this.fetchFull;
            return _this;
        }
        Entries.prototype.componentDidMount = function () {
            this.fetch();
        };
        Entries.prototype.render = function () {
            var groups = this.state.entries;
            var entries = [];
            for (var i = 0, _b = Math.min(this.state.showing, this.state.entries.length); i < _b; i++) {
                entries.push(React.createElement(Entry, { key: i, state: this.props.state, docs: groups[i].doclist.docs[0] }));
            }
            return React.createElement("div", null,
                this.props.mode === 'Embed'
                    ? React.createElement("h4", null,
                        React.createElement("b", null, this.props.group),
                        ": ",
                        this.props.value,
                        " ",
                        React.createElement("small", null,
                            "(",
                            this.state.withCount === 0 ? "No systems with channels!" : this.state.count + "; " + this.state.withCount + " with channels",
                            ")"))
                    : React.createElement("h4", null,
                        React.createElement("b", null, "Search"),
                        ": ",
                        this.props.value,
                        " ",
                        React.createElement("small", null,
                            "(",
                            this.state.count >= 0 ? this.state.count + "; " + this.state.withCount + " with channels" : '?',
                            ")")),
                this.state.isLoading ? React.createElement("div", null, "Loading...") : void 0,
                React.createElement("div", { style: { marginTop: '15px', position: 'relative' } },
                    entries,
                    React.createElement("div", { style: { clear: 'both' } }),
                    this.state.showing < this.state.count
                        ? React.createElement("button", { className: 'btn btn-sm btn-primary btn-block', disabled: this.state.isLoading ? true : false, onClick: this.loadMore }, this.state.isLoading ? 'Loading...' : "Show more (" + (this.state.count > 0 ? this.state.count - this.state.showing : '?') + " remaining; " + Math.max(this.state.withCount - this.state.showing, 0) + " with channels)")
                        : void 0));
        };
        return Entries;
    }(React.Component));
})(ChannelsDB || (ChannelsDB = {}));
