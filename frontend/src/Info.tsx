/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {


    export class Intro extends React.Component<{}, {}> { 
        render() {
            return <div style={{ textAlign: 'center', margin: '60px 0' }}>
                <p>ChannelsDB general info</p>
            </div>;
        }
    }

    export class Info extends React.Component<{}, {}> {
        render() {
            let centerStyle = {
                display: 'block',
                margin: '0 auto',
                marginTop: 30,
            };

            let justify = {
                textAlign: 'justify',
                textJustify: 'inter-word',
            };

            let pdbIdMargin = {
                marginLeft: 50,
            };

            let reference = {
                borderLeft: '2px solid #AAA',
                paddingLeft: 6,
            };

            return <div>
                <h1 style={{ marginTop: 50, textAlign: 'center' }}>Examples</h1>
                <div className='row'>
                    <div className='col-lg-4'>
                        <img style={centerStyle} className='img-circle' src={'assets/img/1ymg_detail.png'} alt='1ymg channel detail' width='140' height='140' />
                        <h2>Water channel architecture</h2>
                        <p>The channel architecture of Aquaporin 0 at 2.2&#8491; resolution highlights residues critical for water permeation regulation.</p>
                        <p><a className='btn btn-default' href='#ex-1ymg' role='button'>View details &raquo;</a></p>
                    </div>

                    <div className='col-lg-4'>
                        <img style={centerStyle} className='img-circle' src={'assets/img/1jj2_detail.png'} alt='1jj2 channel detail' width='140' height='140' />
                        <h2>Ribosomal polypeptide exit tunnel</h2>
                        <p>Ribosomal polypeptide exit tunnel directs a nascent protein from the peptidyl transferase center to the outside of the ribosome.</p>
                        <p><a className='btn btn-default' href='#ex-1jj2' role='button'>View details &raquo;</a></p>
                    </div>
                    <div className='col-lg-4'>
                        <img style={centerStyle} className='img-circle' src='data:image/gif;base64,R0lGODlhAQABAIAAAHd3dwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==' alt='Generic placeholder image' width='140' height='140' />
                        <h2>Cytochrome P450 2D6 substrate tunnel</h2>
                        <p>Fill me Karel!</p>
                        <p><a className='btn btn-default' href='#ex-p450' role='button'>View details &raquo;</a></p>
                    </div>
                </div>

                <hr className='featurette-divider' style={{ margin: '50px 0' }} />

                <div className='row featurette'>
                    <a name="ex-1ymg" />
                    <div className='col-md-7'>
                        <h2 className='featurette-heading'>Aquaporin 0<a style={pdbIdMargin} className='text-muted' href='http://channelsdb.dominiktousek.eu/ChannelsDB/detail/1ymg'>1ymg</a></h2>
                        <p className='lead'>The channel architecture of Aquaporin O at 2.2&#8491; resolution highlights residues critical for water permeation regulation.</p>
                        <p style={justify}>The channel is ~ 30&#8491; long and highlights with some of the residues crucial for its proper function. Selectivity filter (ar/R), which allows water molecules passage through the membrane in a single file (green sticks). Residues providing canonical AQP hydrogen bond acceptor that align watters through the channel in balls and stick model. Finally, Tyr-149 important for channel gating in orange.</p>
                        <p style={reference}><small><a target='_blank' href='https://dx.doi.org/10.1073/pnas.0405274101'>
                            Harries, W. E. C., et. al. <span style={{ fontStyle: 'italic' }}>The channel architecture of aquaporin 0 at a 2.2&#8491; resolution</span>. Proc. Natl. Acad. Sci. 101, 14045–14050 (2004)</a></small></p>
                    </div>
                    <div className='col-md-5'>
                        <img className='featurette-image img-responsive center-block' src={'assets/img/1ymg.png'} width='500' height='500' alt='1ymg detailed channel view' />
                    </div>
                </div>

                <hr className='featurette-divider' style={{ margin: '50px 0' }} />

                <div className='row featurette'>
                    <a name="ex-1jj2" />
                    <div className='col-md-7 col-md-push-5'>
                        <h2 className='featurette-heading'>Large Ribosomal Subunit <a style={pdbIdMargin} className='text-muted' href='http://channelsdb.dominiktousek.eu/ChannelsDB/detail/1jj2'>1jj2</a></h2>
                        <p className='lead'>The ribosomal polypeptide tunnel provides an insight into the release of a nascent polypeptide chain out of the ribosomal complex.</p>
                        <p style={justify}>The exit tunnel is surrounded by arginine side chains (stick model), bearing positive charges as well as RNA backbone phosphate groups (spheres), thus providing fragmental charge along the tunnel, which is necessary to prevent the nasccent peptide from sticking to the channel wall inside the ribosome. Subunits L4, L22 and L39e interacting with the exit tunnel are highlighted in yellow, green and magenta respectivelly.</p>
                        <p style={reference}><small><a target='_blank' href='https://dx.doi.org/10.1016/j.jmb.2006.05.023'>
                            Voss, N. R., et. al. <span style={{ fontStyle: 'italic' }}>The geometry of the ribosomal polypeptide exit tunnel.</span>. J. Mol. Biol. 360, 893–906 (2006)</a></small></p>
                    </div>
                    <div className='col-md-5 col-md-pull-7'>
                        <img className='featurette-image img-responsive center-block' src={'assets/img/1jj2.png'} alt='Generic placeholder image' />
                    </div>
                </div>


                <hr className='featurette-divider' style={{ margin: '50px 0' }} />

                <div className='row featurette'>
                    <a name="ex-p450" />
                    <div className='col-md-7'>
                        <h2 className='featurette-heading'>Cytochrome P450 2D6<a style={pdbIdMargin} className='text-muted' href='http://channelsdb.dominiktousek.eu/ChannelsDB/detail/1tqn'>Fill Me</a></h2>
                        <p className='lead'>Some cool description with reference @Karel</p>
                    </div>
                    <div className='col-md-5'>
                        <img className='featurette-image img-responsive center-block' data-src='holder.js/500x500/auto' alt='Generic placeholder image' />
                    </div>
                </div>
            </div>;
        }
    }
}