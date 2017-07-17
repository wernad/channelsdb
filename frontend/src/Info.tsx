/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {


    export class Intro extends React.Component<{ state: State }, { statistics: any }> {
        private sub: Rx.IDisposable | undefined = void 0;
        state = { statistics: this.props.state.statistics };

        componentDidMount() {
            if (!this.state.statistics) {
                this.sub = this.props.state.statisticsAvailable.subscribe((statistics) => this.setState({ statistics }));
            }
        }

        componentWillUnmount() {
            if (this.sub) {
                this.sub.dispose();
                this.sub = void 0;
            }
        }

        render() {
            const stats = this.state.statistics;
            return <div>
                <div className='row' >
                    <div className='col-lg-12'>
                        <div className='well well-sm text-center' style={{ marginTop: '0', marginBottom: '40px' }}>
                            ChannelsDB last update on <b>{stats ? stats.Date : 'n/a'}</b>
                            &nbsp;<small>contains:</small><b> {stats ? stats.Total : 'n/a'}</b> entries 
                            &nbsp;(<b>{stats ? stats.Reviewed : 'n/a'}</b> <small>reviewed |</small>
                            &nbsp;<b>{stats ? stats.CSA : 'n/a'}</b> <small>with <abbr title='Catalytic Site Atlas'>CSA</abbr> annotation |</small>
                            &nbsp;<b>{stats ? stats.Cofactors : 'n/a'}</b> <small>with cofactors |</small>
                            &nbsp;<b>{stats ? stats.Pores : 'n/a'}</b> <small>transmembrane pores</small>)
                        </div>
                        <div style={{ textAlign: 'left', textJustify: 'inter-word', padding: '0' }}>

                            <p className='lead'>ChannelsDB is a comprehensive and regulary updated resource of channels, pores and tunnels found in biomacromolecules deposited in the
                                <a target='_blank' href='http://www.ebi.ac.uk/pdbe/'> Protein Data Bank</a>. As such, it is a unique service for a channel-related analyses.</p>
                            
                            <p className='text-justify'>
                                The database contains information about channel positions, geometry and physicochemical properties. Additionally, all the entries are crosslinked with
                                the UniProt database a comprehensive high-quality resource of protein function information. Last but not least, all the results are displayed in
                                a clear interactive manner further facilitating data interpretation. </p>                            

                            <hr className='featurette-divider' style={{ margin: '10px 0' }} />

                            <p>If you would like to provide your own research results to be displayed soon as a part of Protein Data Bank in Europe. <a href='mailto:webchemistryhelp@gmail.com'>Get in touch with us!</a>. The application allowing for online annotation will be available later this year.</p>
                        </div>
                    </div>
                </div>
            </div>;
        }
    }

    export class Info extends React.Component<{ state: State }, {}> {

        render() {
            let centerStyle = {
                display: 'block',
                margin: '0 auto',
                marginTop: 0,
            };

            let justify = {
                textAlign: 'justify',
                textJustify: 'inter-word',
            };

            let reference = {
                borderLeft: '2px solid #AAA',
                paddingLeft: 6,
            };

            return <div style={{ marginTop: '0px' }}>
                <Intro state={this.props.state} />
                <div className='row' style={{ marginTop: '30px' }}>
                    <div className='col-lg-12'>
                            <h2 style={{ textAlign: 'center', margin: '0 0 20px 0', fontWeight: 'bold' }}>Examples</h2>
                        <div className='well'>
                            <div className='row'>
                                <div className='col-lg-4'>
                                    <a href='/ChannelsDB/detail/1ymg'>
                                        <img style={centerStyle} className='img-circle' src={'assets/img/1ymg_detail.png'} alt='1ymg channel detail' width='140' height='140' />
                                    </a>
                                    <a href='#ex-1ymg' role='button'><h2>Aquaporin water channel</h2></a>
                                    <p>The pore architecture of Aquaporin 0 at 2.2&#8491; resolution highlights residues critical for water permeation regulation.</p>
                                </div>
                                <div className='col-lg-4'>
                                    <a href='/ChannelsDB/detail/3tbg'>
                                        <img style={centerStyle} className='img-circle' src={'assets/img/3tbg_detail.png'} alt='3tbg channel detail' width='140' height='140' />
                                    </a>
                                    <a href='#ex-3tbg' role='button'><h2>Cytochrome P450 2D6 substrate tunnel</h2></a>
                                    <p>Cytochromes P450 are known for complex net of multiple channels leading towards active site. These channels serve multiple roles in substrate access, product release or hydration pathways.</p>
                                </div>
                                <div className='col-lg-4'>
                                    <a href='/ChannelsDB/detail/1jj2'>
                                        <img style={centerStyle} className='img-circle' src={'assets/img/1jj2_detail.png'} alt='1jj2 channel detail' width='140' height='140' />
                                    </a>
                                    <a href='#ex-1jj2' role='button'><h2>Ribosomal polypeptide exit tunnel</h2></a>
                                    <p>Ribosomal polypeptide exit tunnel directs a nascent protein from the peptidyl transferase center to the outside of the ribosome.</p>
                                </div>
                            </div>
                            <div className='row'>
                                <div className='col-lg-4'>
                                    <a className='btn btn-block btn-default' href='#ex-1ymg' role='button'>View details &raquo;</a>
                                </div>
                                <div className='col-lg-4'>
                                    <a className='btn btn-block btn-default' href='#ex-p450' role='button'>View details &raquo;</a>
                                </div>
                                <div className='col-lg-4'>
                                    <a className='btn btn-block btn-default' href='#ex-1jj2' role='button'>View details &raquo;</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className='row featurette' style={{ marginTop: '40px' }}>
                    <a name='ex-1ymg' />
                    <div className='col-md-7'>
                        <a href='/ChannelsDB/detail/1ymg'><h2 className='featurette-heading'>Aquaporin O <span className='text-muted'>(1ymg)</span></h2></a>
                        <p className='lead'>The pore architecture of Aquaporin O at 2.2&#8491; resolution highlights residues critical for water permeation regulation.</p>
                        <p style={justify}>The channel is ~ 30&#8491; long and highlights with some of the residues crucial for its proper function. Selectivity filter (ar/R), which allows water molecules passage through the membrane in a single file (green sticks). Residues providing canonical AQP hydrogen bond acceptor that align watters through the channel in balls and stick model. Finally, Tyr-149 important for channel gating in orange.</p>
                        <p style={reference}><small><a target='_blank' href='https://dx.doi.org/10.1073/pnas.0405274101'>
                            Harries, W. E. C., et. al. <span style={{ fontStyle: 'italic' }}>The channel architecture of aquaporin 0 at a 2.2&#8491; resolution</span>. Proc. Natl. Acad. Sci. 101, 14045–14050 (2004)</a></small></p>
                    </div>
                    <div className='col-md-5'>
                        <img className='featurette-image img-responsive center-block' src={'assets/img/1ymg.png'} width='500' height='500' alt='1ymg detailed channel view' />
                    </div>
                </div>

                <hr className='featurette-divider' style={{ margin: '40px 0' }} />


                <div className='row featurette'>
                    <a name='ex-p450' />
                    <div className='col-md-7 col-md-push-5'>
                        <a href='/ChannelsDB/detail/3tbg'><h2 className='featurette-heading'>Cytochrome P450 2D6 <span className='text-muted'>(3tbg)</span></h2></a>
                        <p className='lead'>Cytochromes P450 are known for complex net of multiple channels leading towards active site. These channels serve multiple roles in substrate access, product release or hydration pathways.</p>
                        <p style={justify}>Cytochrome  P450  2D6  contributes  significantly  to  the  metabolism  of  >15%  of  the  200  most marketed drugs. Cytochrome P450 2D6 structure shows a second molecule of thioridazine bound in an expanded substrate access channel (channel 2f according to <a href='https://doi.org/10.1016/j.bbagen.2006.07.005' target='_blank'>Cojocaru et al. classification</a>  antechamber  with  its  piperidine  moiety  forming  a charge-stabilized hydrogen bond with Glu-222.</p>
                        <p style={reference}><small><a target='_blank' href='https://dx.doi.org/10.1074/jbc.M114.627661'>
                            Wang, A., et al. <span style={{ fontStyle: 'italic' }}>Contributions of Ionic Interactions and Protein Dynamics to Cytochrome P450 2D6 (CYP2D6) Substrate and Inhibitor Binding</span> J.Biol.Chem. 290: 5092-5104 (2015)</a></small></p>
                    </div>
                    <div className='col-md-5 col-md-pull-7'>
                        <img className='featurette-image img-responsive center-block' src={'assets/img/3tbg.png'} alt='Cytochrome P450 substrate channel details' />
                    </div>
                </div>

                <hr className='featurette-divider' style={{ margin: '40px 0' }} />

                <div className='row featurette'>
                    <a name='ex-1jj2' />
                    <div className='col-md-7 '>
                        <a href='/ChannelsDB/detail/1jj2'><h2 className='featurette-heading'>Large Ribosomal Subunit <span className='text-muted'>(1jj2)</span></h2></a>
                        <p className='lead'>The ribosomal polypeptide tunnel provides an insight into the release of a nascent polypeptide chain out of the ribosomal complex.</p>
                        <p style={justify}>The exit tunnel is surrounded by arginine side chains (stick model), bearing positive charges as well as RNA backbone phosphate groups (spheres), thus providing fragmental charge along the tunnel, which is necessary to prevent the nasccent peptide from sticking to the channel wall inside the ribosome. Subunits L4, L22 and L39e interacting with the exit tunnel are highlighted in yellow, green and magenta respectivelly.</p>
                        <p style={reference}><small><a target='_blank' href='https://dx.doi.org/10.1016/j.jmb.2006.05.023'>
                            Voss, N. R., et. al. <span style={{ fontStyle: 'italic' }}>The geometry of the ribosomal polypeptide exit tunnel.</span>. J. Mol. Biol. 360, 893–906 (2006)</a></small></p>
                    </div>
                    <div className='col-md-5 '>
                        <img className='featurette-image img-responsive center-block' src={'assets/img/1jj2.png'} alt='Polypeptide exit tunnel' />
                    </div>
                </div>

                <hr className='featurette-divider' style={{ margin: '40px 0' }} />

                <img className='row featurette col-md-offset-6' src={'assets/img/elixirlogo.png'} alt="ELIXIR logo" height='70' />
                <small className='row featurette'>
                     ChannelsDB is a part of services provided by <a href="https://www.elixir-czech.cz/" target="_blank">ELIXIR</a> &ndash;
                     European research infrastructure for biological information. For other services provided by ELIXIR's Czech Republic Node visit <a href="https://www.elixir-czech.cz/services" target="_blank">www.elixir-czech.cz/services</a>.
                </small>
            </div>;
        }
    }
}