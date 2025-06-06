/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

import { ajaxGetJson, fetchAjax, RequestPool } from "./Utils";

export interface DBContent {
    pdb: { [id: string]: any };
    alphafill: { [id: string]: any };
}

export type GenericStatistics = { [key: string]: number };
export type ExtendedStatistics = { [key: string]: number | string };

export type StatisticsData = {
    "methods": GenericStatistics,
    "length": ExtendedStatistics,
    "bottleneck": GenericStatistics,
    "top_types": GenericStatistics,
    "top_proteins": GenericStatistics,
    "top_residues": GenericStatistics,
    "date": string,
    "entries_count": number
}

export interface State {
    apiAvailable: Rx.BehaviorSubject<boolean>;
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

export type ViewState = ViewState.Info | ViewState.Seached | ViewState.Entries | ViewState.Filter | ViewState.Loading | ViewState.Error;

export type FilterData = {
  min_radius?: number,
  max_radius?: number,
  min_distance?: number,
  max_distance?: number,
  min_bottleneck?: number,
  limit?: number,
  offset?: number
}

export namespace ViewState {
    export type Info = { kind: 'Info' };
    export type Loading = { kind: 'Loading', message: string };
    export type Seached = { kind: 'Searched', data: any };
    export type Entries = { kind: 'Entries', term: string };
    export type Filter = { kind: 'Filter', term: string[]};
    export type Error = { kind: 'Error', message: string };
}

export function updateViewState(state: State, viewState: ViewState) {
    state.viewState = viewState;
    state.stateUpdated.onNext(void 0);
}

export function initState(): State {
    const state: State = {
        apiAvailable: new Rx.BehaviorSubject<boolean>(false),
        statistics: void 0 as any,
        statisticsAvailable: new Rx.BehaviorSubject<any>(void 0),
        searchedTerm: '',
        searchTerm: new Rx.Subject<string>(),
        viewState: { kind: 'Info' },
        stateUpdated: new Rx.Subject<undefined>(),
        fullSearch: new Rx.Subject<undefined>(),
        channelsUrl: "/api/v1",
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
    
    checkAPI(state);
    getStatistics(state);

    return state;
}

async function fetchAndHandleNotFound(url: string) {
    try {
        const result =  await ajaxGetJson(url)
        return result;
    } catch (e) {
        const result = undefined;
        return result;
    }
}
async function checkAPI(state: State) {
    try {
        
        const result = await ping(state);
        if (result === true) {
            state.apiAvailable.onNext(true);
        }
    } catch (e) {
        console.log(`Unable to ping API, re-trying in 2 seconds. Error: ${e}`)
        setTimeout(() => checkAPI(state), 2000);
    }    
}

async function getStatistics(state: State) {
    try {
        if (state.statistics) {
            state.statisticsAvailable.onNext(state.statistics);
            return;
        }

        const methods = await fetchAndHandleNotFound(`${state.channelsUrl}/statistics/methods`);
        const length = await fetchAndHandleNotFound(`${state.channelsUrl}/statistics/length`);
        const bottleneck = await fetchAndHandleNotFound(`${state.channelsUrl}/statistics/bottleneck`);
        const topTypes = await fetchAndHandleNotFound(`${state.channelsUrl}/statistics/top_types`);
        const topProteins = await fetchAndHandleNotFound(`${state.channelsUrl}/statistics/top_proteins`);
        const topResidues = await fetchAndHandleNotFound(`${state.channelsUrl}/statistics/top_residues`);
        
        const data = {
            "entries_count": methods !== undefined ? methods.entries_count : undefined,
            "date": methods !== undefined ? methods.date : undefined,
            "methods": methods !== undefined ? methods.statistics : undefined,
            "length": length !== undefined ? length.statistics : undefined,
            "bottleneck": bottleneck !== undefined ? bottleneck.statistics : undefined,
            "top_types": topTypes !== undefined ? topTypes.statistics : undefined,
            "top_proteins": topProteins !== undefined ? topProteins.statistics : undefined,
            "top_residues": topResidues !== undefined ? topResidues.statistics : undefined,
        };

        state.statistics = data;
        state.statisticsAvailable.onNext(data);
    } catch (e) {
        setTimeout(() => getStatistics(state), 2000);
    }
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

async function sortGroups(state: State, groups: any) {
    const withChannels = [], withoutChannels = [], counts: {}[] = [];

    for (const group of groups) {
        const id = group.doclist.docs[0].pdb_id;
        const url = `${state.channelsUrl}/statistics/methods/${id}`;

        const fetched = await ajaxGetJson(url);
        counts.push(fetched);
        if (fetched.entries_count > 0) {
            withChannels.push(group);
        }
        else {
            withoutChannels.push(group);
        }
    }
    return { entries: withChannels.concat(withoutChannels), withCount: withChannels.length, withoutCount: withoutChannels.length, counts: counts };
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

export async function fetchFilter(state: State, filter: FilterData) {
    const params = new URLSearchParams();
    
    const camelToSnakeCase = (str: string) => str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);   

    for (const key in filter) {
        if (filter.hasOwnProperty(key)) {
            const value = filter[key as keyof FilterData];
            if (value !== undefined && value !== null && value.toString() !== '') {
                const snakeKey = camelToSnakeCase(key);
                params.append(snakeKey, value.toString());
            }
        }
    };

    params.append('limit', ROW_COUNT.toString())
    
    const url = `${state.channelsUrl}/structures/filter?${params.toString()}`
    const data = await ajaxGetJson(url);
    return data;
}

export async function ping(state: State) {
    const url = `${state.channelsUrl}/health/ping`;
    const result = await fetchAjax(url)

    const req = (result.target as XMLHttpRequest);
    if (req.status !== 200) {
        throw Error('API is not available.')
    }

    return true;
}