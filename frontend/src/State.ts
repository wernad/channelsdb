/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {
    
    export interface State {
        searchedTerm: string,
        searchTerm: Rx.Subject<string>,
        viewState: ViewState,
        stateUpdated: Rx.Subject<undefined>,
        fullSearch: Rx.Subject<undefined>
    }

    export interface EntryGroup {
        header: string,
        numPdbEntries: number,
        varName: string,
        value: string
    }

    export type ViewState = ViewState.Info | ViewState.Seached | ViewState.Entries | ViewState.Loading | ViewState.Error

    export namespace ViewState {
        export type Info = { kind: 'Info' }
        export type Loading = { kind: 'Loading', message: string }
        export type Seached = { kind: 'Searched', data: any }
        export type Entries = { kind: 'Entries', term: string }
        export type Error = { kind: 'Error', message: string }
    }

    export function updateViewState(state: State, viewState: ViewState) {
        state.viewState = viewState;
        state.stateUpdated.onNext(void 0);
    }

    export function initState(): State {
        const state: State = {
            searchedTerm: '',
            searchTerm: new Rx.Subject<string>(),
            viewState: { kind: 'Info' },
            stateUpdated: new Rx.Subject<undefined>(),
            fullSearch: new Rx.Subject<undefined>()
        }

        state.searchTerm
            .map(t => t.trim())
            .distinctUntilChanged()
            .debounce(250)
            .forEach(t => {
                if (t.length > 2) {
                    search(state, t).takeUntil(Rx.Observable.merge(state.searchTerm, state.fullSearch)).subscribe(
                        data => { state.searchedTerm = t; updateViewState(state, { kind: 'Searched', data }) }, 
                        err => updateViewState(state, { kind: 'Error', message: '' + err }))
                } else {
                    updateViewState(state, { kind: 'Info' })
                }
            });

        return state;
    }

    function search(state: State, term: string) {
        updateViewState(state, { kind: 'Loading', message: 'Searching...' });
        const s = new Rx.Subject<any>();
        ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb-autocomplete/select?rows=20000&json.nl=map&group=true&group.field=category&group.limit=28&fl=value,num_pdb_entries,var_name&sort=category+asc,num_pdb_entries+desc&q=value:${encodeURIComponent(`"${term}*"`)}~10&wt=json`)
            .then(data => { s.onNext(data); s.onCompleted() })
            .catch(err => { s.onError(err); s.onCompleted() })
        return s;
    }

    export async function searchPdbCategory(term: string, var_name: string, start: number) {
        const data = await ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb-autocomplete/select?rows=28&start=${start}&json.nl=map&group.limit=-1&fl=value,num_pdb_entries,var_name&sort=category+asc,num_pdb_entries+desc&fq=var_name:${var_name}&q=value:${encodeURIComponent(`"${term}*"`)}~10&wt=json`);
        return data.response.docs;
    }

    export async function fetchPdbEntries(var_name: string, value: string, start: number, count: number) {        
        const data = await ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb/select?q=*:*&group=true&group.field=pdb_id&start=${start}&rows=${count}&group.ngroups=true&fl=pdb_id,title,experimental_method,organism_scientific_name,resolution,entry_organism_scientific_name&json.nl=map&fq=${encodeURIComponent(var_name)}:"${encodeURIComponent(value)}"&sort=overall_quality+desc&wt=json`)
        return data.grouped.pdb_id.groups;
    }

    export async function fetchPdbText(value: string, start: number, count: number) {        
        const data = await ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb/select?q=*:*&group=true&group.field=pdb_id&start=${start}&rows=${count}&group.ngroups=true&fl=pdb_id,title,experimental_method,organism_scientific_name,resolution,entry_organism_scientific_name&json.nl=map&fq=text:"${encodeURIComponent(value)}"&sort=overall_quality+desc&wt=json`)
        return { groups: data.grouped.pdb_id.groups, matches: (data as any).grouped.pdb_id.ngroups };
    }
}