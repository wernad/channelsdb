/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {

    export interface DBContent {
        pdb: { [id: string]: any };
        alphafill: { [id: string]: any };
    }

    export interface State {
        dbContent: DBContent;
        dbContentAvailable: Rx.BehaviorSubject<boolean>;
        statistics: any;
        statisticsAvailable: Rx.BehaviorSubject<any>;
        searchedTerm: string;
        searchTerm: Rx.Subject<string>;
        viewState: ViewState;
        stateUpdated: Rx.Subject<undefined>;
        fullSearch: Rx.Subject<undefined>;
        channelsUrl: string;
    }

    export interface EntryGroup {
        header: string;
        numPdbEntries: number;
        varName: string;
        value: string;
    }

    export type ViewState = ViewState.Info | ViewState.Seached | ViewState.Entries | ViewState.Loading | ViewState.Error;

    export namespace ViewState {
        export type Info = { kind: 'Info' };
        export type Loading = { kind: 'Loading', message: string };
        export type Seached = { kind: 'Searched', data: any };
        export type Entries = { kind: 'Entries', term: string };
        export type Error = { kind: 'Error', message: string };
    }

    export function updateViewState(state: State, viewState: ViewState) {
        state.viewState = viewState;
        state.stateUpdated.onNext(void 0);
    }

    export function initState(): State {
        const state: State = {
            dbContent: void 0 as any,
            dbContentAvailable: new Rx.BehaviorSubject<boolean>(false),
            statistics: void 0 as any,
            statisticsAvailable: new Rx.BehaviorSubject<any>(void 0),
            searchedTerm: '',
            searchTerm: new Rx.Subject<string>(),
            viewState: { kind: 'Info' },
            stateUpdated: new Rx.Subject<undefined>(),
            fullSearch: new Rx.Subject<undefined>(),
            channelsUrl: "http://channelsdb2.biodata.ceitec.cz",
        };

        const interrupt = Rx.Observable.merge(state.searchTerm as Rx.Observable<any>, state.fullSearch as Rx.Observable<any>);

        state.searchTerm
            .do(() => RequestPool.abort('data'))
            .map((t) => t.trim())
            .distinctUntilChanged()
            .concatMap((t) => Rx.Observable.timer(250).takeUntil(interrupt).map((_) => t))
            .forEach((t) => {
                if (t.length > 2) {
                    search(state, t).takeUntil(interrupt).subscribe(
                        (data) => { state.searchedTerm = t; updateViewState(state, { kind: 'Searched', data }); },
                        (err) => { if (err !== 'Aborted') updateViewState(state, { kind: 'Error', message: '' + err }); });
                } else {
                    updateViewState(state, { kind: 'Info' });
                }
            });

        initSearch(state);
        getStatistics(state);

        return state;
    }

    async function initSearch(state: State) {
        try {
            const content = await ajaxGetJson(`${state.channelsUrl}/content`);
            state.dbContent = { pdb: content.PDB, alphafill: content.AlphaFill };
            state.dbContentAvailable.onNext(true);
        } catch (e) {
            setTimeout(() => initSearch(state), 2000);
        }
    }

    async function getStatistics(state: State) {
        try {
            if (state.statistics) {
                state.statisticsAvailable.onNext(state.statistics);
                return;
            }
            const content = await ajaxGetJson(`${state.channelsUrl}/statistics`); 
            state.statistics = content;
            state.statisticsAvailable.onNext(content);
        } catch (e) {
            setTimeout(() => getStatistics(state), 2000);
        }
    }

    function sortSearchData(state: State, data: any) {

    }

    function search(state: State, term: string) {
        RequestPool.abort('data');
        updateViewState(state, { kind: 'Loading', message: 'Searching...' });
        const s = new Rx.Subject<any>();
        ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb-autocomplete/select?rows=1000000&json.nl=map&group=true&group.field=category&group.limit=28&fl=value,num_pdb_entries,var_name&sort=category+asc,num_pdb_entries+desc&q=value:${encodeURIComponent(`"${term}*"`)}~10&wt=json`, 'data')
            .then((data) => { s.onNext(data); s.onCompleted(); })
            .catch((err) => { s.onError(err); s.onCompleted(); });
        return s;
    }

    export async function searchPdbCategory(term: string, var_name: string, start: number) {
        RequestPool.abort('data');
        const data = await ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb-autocomplete/select?rows=28&start=${start}&json.nl=map&group.limit=-1&fl=value,num_pdb_entries,var_name&sort=category+asc,num_pdb_entries+desc&fq=var_name:${var_name}&q=value:${encodeURIComponent(`"${term}*"`)}~10&wt=json`, 'data');
        return data.response.docs;
    }

    const ROW_COUNT = 1000000;

    const toLowerCache = {} as any;
    export function toLower(str: string) {
        let ret = toLowerCache[str];
        if (ret) return ret;
        ret = str.toLowerCase();
        toLowerCache[str] = ret;
        return ret;
    }

    function sortGroups(state: State, groups: any) {
        const withChannels = [], withoutChannels = [];
        const content = state.dbContent.pdb; //TODO set also alphafill

        for (const group of groups) {
            if (content[toLower(group.doclist.docs[0].pdb_id)]) withChannels.push(group);
            else withoutChannels.push(group);
        }

        return { entries: withChannels.concat(withoutChannels), withCount: withChannels.length, withoutCount: withoutChannels.length };
    }

    export async function fetchPdbEntries(state: State, var_name: string, value: string) {
        const data = await ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb/select?q=*:*&group=true&group.field=pdb_id&start=${0}&rows=${ROW_COUNT}&group.ngroups=true&fl=pdb_id,title,experimental_method,organism_scientific_name,resolution,entry_organism_scientific_name&json.nl=map&fq=${encodeURIComponent(var_name)}:"${encodeURIComponent(value)}"&sort=overall_quality+desc&wt=json`, 'data');
        return sortGroups(state, data.grouped.pdb_id.groups);
    }

    export async function fetchPdbText(state: State, value: string) {
        RequestPool.abort('data');
        const data = await ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb/select?q=*:*&group=true&group.field=pdb_id&start=${0}&rows=${ROW_COUNT}&group.ngroups=true&fl=pdb_id,title,experimental_method,organism_scientific_name,resolution,entry_organism_scientific_name&json.nl=map&fq=text:"${encodeURIComponent(value)}"&sort=overall_quality+desc&wt=json`, 'data');
        return sortGroups(state, data.grouped.pdb_id.groups);
    }
}