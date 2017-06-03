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
                {/*<div className="masthead">
                    <h3 className="text-muted">ChannelsDB</h3>
                    <nav>
                        <ul className="nav nav-justified">
                            <li className="active"><a href="#">DB</a></li>
                            <li><a href="#">MOLE</a></li>
                            <li><a href="#">Contribute</a></li>
                            <li><a href="#">About</a></li>
                        </ul>
                    </nav>
                </div>*/}

                <nav className="navbar navbar-default">
                    <div className="container-fluid">
                        <div className="navbar-header">
                            <a className="navbar-brand" href="#">ChannelsDB</a>
                        </div>
                        <div id="navbar" className="navbar-collapse collapse">
                            {/*<ul className="nav navbar-nav">
                                <li className="active"><a href="#">DB</a></li>
                            </ul>*/}
                            <ul className="nav navbar-nav navbar-right">
                                <li><a href="#">MOLE</a></li>
                                <li><a href="#">About</a></li>
                                <li><a href="#">Contribute</a></li>
                            </ul>
                        </div>
                    </div>
                </nav>

                <MainView {...this.props} />

                <hr className="featurette-divider" />

                <footer>
                    <p className='pull-right' style={{ color: '#999' }}>&copy; 2017 Lukáš Pravda &amp; David Sehnal</p>
                </footer>
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
                    <input type='text' className="form-control" style={{ fontWeight: 'bold' }} placeholder="Search..." onChange={e => this.props.state.searchTerm.onNext(e.target.value)} />
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
            return groups.map((g: any, i: number) => <SearchGroup key={g.groupValue + '--' + i} {...this.props} group={g} />);
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

    export class SearchGroup extends React.Component<GlobalProps & { group: any }, { expanded: boolean, docs: any[], isLoading: boolean, entries?: { group: string, value: string, var_name: string, count: number } }> {
        state = { expanded: false, docs: [] as any[], isLoading: false, entries: void 0 as any as { group: string, value: string, var_name: string, count: number } }

        private toggle = (e: React.MouseEvent<any>) => {
            e.preventDefault();
            this.setState({ expanded: !this.state.expanded });
        }

        private showEntries = (e: React.MouseEvent<HTMLAnchorElement>) => {
            e.preventDefault();
            const value = (e.target as HTMLAnchorElement).getAttribute('data-value')!;
            const var_name = (e.target as HTMLAnchorElement).getAttribute('data-var')!;
            const count = +(e.target as HTMLAnchorElement).getAttribute('data-count')!;
            this.setState({ entries: { group: this.props.group.groupValue, value, var_name, count } });
        }

        private loadMore = async () => {
            try {
                this.setState({ isLoading: true });
                const data = await loadGroupDocs('', '', this.state.docs.length, 25);
                this.setState({ isLoading: false, docs: this.state.docs.concat(data) });
            } catch (e) {
                this.setState({ isLoading: false });
            } 
        }

        componentDidMount() {
            this.setState({ docs: this.props.group.doclist.docs })
        }

        private entry(d: any, i: any) {
            return <div key={d.value + d.var_name + '--' + i}>
                <a href='#' data-value={d.value} data-var={d.var_name} data-count={d.num_pdb_entries} onClick={this.showEntries} title={`${d.value}`}>{d.value}</a> 
                <div className='count'>{d.num_pdb_entries}</div>
            </div>
        }

        render() {
            const g = this.props.group;

            return <div style={{ marginBottom: '10px' }}>
                <div className='group-header'><button className='btn btn-default btn-block' onClick={this.toggle}><span className={`glyphicon glyphicon-${this.state.expanded ? 'minus' : 'plus'}`} aria-hidden="true"></span> <span>{g.groupValue}</span> ({g.doclist.numFound})</button></div>
                <div className='group-list-wrap' style={{ display: this.state.entries ? 'none' : 'block' }}>
                    <div className='group-list' style={{ display: this.state.expanded ? 'block' : 'none' }}>
                        {this.state.docs.map((d: any, i: number) => this.entry(d, i)) }
                        {this.state.docs.length < g.doclist.numFound
                            ? <div style={{ padding: 0 }}>
                                <button style={{ width: '100%', display: 'block' }} className='btn btn-xs btn-primary' disabled={this.state.isLoading ? true : false} onClick={this.loadMore}>{this.state.isLoading ? 'Loading...' : 'Show more'}</button>
                            </div>
                            : void 0}
                    </div>
                    <div style={{ clear: 'both' }} />
                </div>
                { this.state.entries 
                ? <div className='entry-list-wrap'>
                    <button className='btn btn-block btn-primary' onClick={() =>this.setState({ entries: void 0 })}><span className={`glyphicon glyphicon-chevron-left`} aria-hidden="true"></span></button>
                    <Entries state={this.props.state} {...this.state.entries!} />
                  </div> 
                : void 0 }
            </div>
        }
    }

    export class Entries extends React.Component<GlobalProps & { group: string, value: string, var_name: string, count: number }, { isLoading: boolean, entries: any[] }> {
        state = { isLoading: false, entries: [] as any[] }
        
        private fetch = async () => {
            try {
                this.setState({ isLoading: true })
                const data = await fetchPdbEntries(this.props.var_name, this.props.value, this.state.entries.length, 5);
                this.setState({ isLoading: false, entries: this.state.entries.concat(data) });
            } catch (e) {
                this.setState({ isLoading: false });
            }
        }

        componentDidMount() {
            this.fetch();
        }

        private entry(e: any, i: number) {
            const docs = e.doclist.docs[0];
            return <div key={docs.pdb_id + '--' + i} className='well'>
                <ul>
                    <li>PDB ID: {docs.pdb_id}</li>
                    <li>Name: {docs.title || 'n/a'}</li>
                    <li>Experiment Method: {(docs.experimental_method || ['n/a']).join(', ')} | Resolution: {docs.resolution || 'n/a'}</li>
                    <li>Organism: {(docs.organism_scientific_name || ['n/a']).join(', ')}</li>
                </ul>
            </div>
        }

        render() {
            const groups = this.state.entries;

            return <div>
                <h4><b>{this.props.group}</b>: {this.props.value} <small>({this.props.count})</small></h4>
                <div style={{ marginTop: '15px' }}>
                    {groups.map((g: any, i: number) => this.entry(g, i))}
                    {this.state.entries.length < this.props.count
                        ? <button className='btn btn-sm btn-primary btn-block' disabled={this.state.isLoading ? true : false} onClick={this.fetch}>{this.state.isLoading ? 'Loading...' : 'Show more'}</button>
                        : void 0}
                </div>
            </div>;
        }
    }
}