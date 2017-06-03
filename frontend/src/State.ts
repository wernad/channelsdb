/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {
    
    export interface State {
        searchTerm: Rx.Subject<string>,
        viewState: ViewState,
        stateUpdated: Rx.Subject<undefined>
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
        export type Entries = { kind: 'Entries', pageIndex: number, pageCount: number, pages: { [page: number]: any }, group: string,  value: string, searched: Seached }
        export type Error = { kind: 'Error', message: string }
    }

    export function updateViewState(state: State, viewState: ViewState) {
        state.viewState = viewState;
        state.stateUpdated.onNext(void 0);
    }

    export function initState(): State {
        const state: State = {
            searchTerm: new Rx.Subject<string>(),
            viewState: { kind: 'Info' },
            stateUpdated: new Rx.Subject<undefined>()
        }

        state.searchTerm
            .distinctUntilChanged()
            .debounce(250)
            .forEach(t => {
                if (t.trim().length > 0) {
                    search(state, t).takeUntil(state.searchTerm).subscribe(
                        data => updateViewState(state, { kind: 'Searched', data }), 
                        err => updateViewState(state, { kind: 'Error', message: '' + err }))
                } else {
                    updateViewState(state, { kind: 'Info' })
                }
            });

        return state;
    }

    function search(state: State, term: string) {
        updateViewState(state, { kind: 'Loading', message: 'Searching...' });
        const s = new Rx.Subject<object>();
        ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb-autocomplete/select?rows=20000&json.nl=map&group=true&group.field=category&group.limit=25&fl=value,num_pdb_entries,var_name&sort=category+asc,num_pdb_entries+desc&q=value:${term}*~10&wt=json`)
            .then(data => { s.onNext(data); s.onCompleted() })
            .catch(err => { s.onError(err); s.onCompleted() })
        return s;
    }

    export async function showPdbEntries(state: State, var_name: string, value: string, group: string) {        
        try {
            const searched = state.viewState as ViewState.Seached;
            updateViewState(state, { kind: 'Loading', message: 'Loading entries...' });
            console.log(var_name, value, group);
            const data = await ajaxGetJson(`https://www.ebi.ac.uk/pdbe/search/pdb/select?q=*:*&group=true&group.field=pdb_id&rows=100&group.ngroups=true&fl=pdb_id,title,experimental_method,organism_scientific_name,resolution,entry_organism_scientific_name&json.nl=map&fq=${encodeURIComponent(var_name)}:"${encodeURIComponent(value)}"&sort=overall_quality+desc&wt=json`)
            console.log('pdbentries', data);
            updateViewState(state, { kind: "Entries", pageIndex: 0, pageCount: 1, pages: { 0: data }, searched, group, value });
        } catch (e) {
            updateViewState(state, { kind: 'Error', message: '' + e });
        }
    }
}