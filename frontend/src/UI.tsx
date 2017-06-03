/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {

    export function renderUI(target: HTMLElement) {
        ReactDOM.render(<App state={initState()} />, target);
    }

    type GlobalProps = { state: State }

    export class App extends React.Component<GlobalProps, {}> {

        componentDidMount() {
            this.load();
        }

        load() {
            
        }

        render() {
            return <div className='container'>
                <div className="masthead">
                    <h3 className="text-muted">ChannelsDB</h3>
                    <nav>
                        <ul className="nav nav-justified">
                            <li className="active"><a href="#">DB</a></li>
                            <li><a href="#">MOLE</a></li>
                            <li><a href="#">Contribute</a></li>
                            <li><a href="#">About</a></li>
                        </ul>
                    </nav>
                </div>

                <MainView {...this.props} />
            </div>
        }
    }

    export class MainView extends React.Component<GlobalProps, {}> {
        
        render() {
            return <div style={{ marginTop: '35px' }}>     
                <div className='row'>           
                    <div className="col-lg-12"><SearchBox {...this.props} /></div>
                </div>
                <div className='row'>
                    <div className="col-lg-12"><StateView {...this.props} /></div>
                </div>
            </div>
        }
    }

    export class StateView extends React.Component<GlobalProps, {}> {        

        componentDidMount() {
            this.props.state.stateUpdated.subscribe(() => this.forceUpdate());
        }

        render() {
            const state = this.props.state.viewState;
            try {
                switch (state.kind) {
                    case 'Info': return <Info />;
                    case 'Loading': return <div>{state.message}</div>;
                    case 'Searched': return <SearchResults {...this.props} />;
                    case 'Entries': return <Entries {...this.props} />
                    case 'Error': return <div>Error: {state.message}</div>;
                    default: return <div>Should not happen ;)</div>;
                }
            } catch (e) {
                return <div>Error: {'' + e}</div>;
            }
        }
    }

    export class SearchBox extends React.Component<GlobalProps, {}> {
        render() {
            return <form>
                <div className="form-group form-group-lg">
                    <input type='text' className="form-control" placeholder="Search..." onChange={e => this.props.state.searchTerm.onNext(e.target.value)} />
                </div>
            </form>
        }
    }

    export class Info extends React.Component<{}, {}> {
        render() {
            return <div>
                Examples etc go here.
            </div>
        }
    }

    export class SearchResults extends React.Component<GlobalProps, {}> {
        private empty() {
            return <div>No results</div>;
        }

        private groups() {
            const data = (this.props.state.viewState as ViewState.Seached).data;
            const groups = data.grouped.category.groups;
            return groups.map((g: any) => <SearchGroup key={g.groupValue} {...this.props} group={g} />);
        }

        render() {
            try {
                const data = (this.props.state.viewState as ViewState.Seached).data;
                console.log(data);
                if (!data.grouped.category.groups.length) return this.empty();
                return <div>{this.groups()}</div>;
            } catch (e) {
                return this.empty();
            }
        }
    }

    export class SearchGroup extends React.Component<GlobalProps & { group: any }, { expanded: boolean }> {
        state = { expanded: false }

        private toggle = (e: React.MouseEvent<any>) => {
            e.preventDefault();
            this.setState({ expanded: !this.state.expanded });
        }

        private showEntries = (e: React.MouseEvent<HTMLAnchorElement>) => {
            e.preventDefault();
            const value = (e.target as HTMLAnchorElement).getAttribute('data-value')!;
            const var_name = (e.target as HTMLAnchorElement).getAttribute('data-var')!;            
            showPdbEntries(this.props.state, var_name, value, this.props.group.groupValue);
        }

        render() {
            const g = this.props.group;

            return <div>
                <h4><button className='btn btn-link' onClick={this.toggle}><span className={`glyphicon glyphicon-${this.state.expanded ? 'minus' : 'plus'}`} aria-hidden="true"></span></button> {g.groupValue} <small>({g.doclist.numFound})</small></h4>
                {this.state.expanded
                    ? <div className='group-list'>
                        {g.doclist.docs.map((d: any) => <div key={d.value}><a href='#' data-value={d.value} data-var={d.var_name} onClick={this.showEntries}>{d.value} ({d.num_pdb_entries})</a></div>)}
                    </div>
                    : void 0}
            </div>
        }        
    }

    export class Entries extends React.Component<GlobalProps, {}> {        
        // private showEntries = (e: React.MouseEvent<HTMLAnchorElement>) => {
        //     e.preventDefault();
        //     const value = (e.target as HTMLAnchorElement).getAttribute('data-value')!;
        //     const var_name = (e.target as HTMLAnchorElement).getAttribute('data-var')!;
        //     //showPdbEntries(this.props.state, var_name, value);
        // }

        private entry(e: any) {
            const docs = e.doclist.docs[0];
            return <div key={e.groupValue} className='well'>
                <ul>
                    <li>PDB ID: {docs.pdb_id}</li>
                    <li>Name: {docs.title || 'n/a'}</li>
                    <li>Experiment Method: {(docs.experimental_method || ['n/a']).join(', ')} | Resolution: {docs.resolution || 'n/a'}</li>
                    <li>Organism: {(docs.organism_scientific_name || [ 'n/a']).join(', ')}</li>
                </ul>
            </div>
        }

        render() {
            const data = (this.props.state.viewState as ViewState.Entries);
            const page = data.pages[data.pageIndex];
            const groups = page.grouped.pdb_id.groups;

            return <div>
                <button className='btn btn-lg btn-block btn-primary' onClick={() => updateViewState(this.props.state, data.searched)}>Back</button>
                <h2><b>{data.group}</b>: {data.value}</h2>
                <div style={{ marginTop: '15px' }}>
                    {groups.map((g: any) => this.entry(g))}
                </div>
            </div>
        }        
    }
}