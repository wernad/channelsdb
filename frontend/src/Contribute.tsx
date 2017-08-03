/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {
    export class Contribute extends React.Component<{}, {}> {
        submitAnnotation(){
            alert("Clicked, yay")
        };
        
        render() {
            return <div style={{ margin: '60px 0 0 20px' }}>

                <h1 className='text-center'>Contribute</h1>                
                    <p>If you would like to contribute to the ChannelsDB or point out not yet annotated systems with known channels, please use the form below, until the online annotation tool is ready by the end of 2017:</p>
                    <form className='form-horizontal'>
                        <div className='form-group'>
                            <label className='control-label col-sm-2' htmlFor='pdbId'>PDB identifier</label>
                            <div className='col-sm-10'>
                                <input type='text' className='form-control' id='pdbId' placeholder='1tqn' />                            
                            </div>
                        </div>
                        <div className='form-group'>
                            <label className='control-label col-sm-2' htmlFor='litReference'>Literature reference</label>
                            <div className='col-sm-10'>
                                <input type='text' className='form-control' id='litReference' placeholder='Doi or Pubmed ID (e.g. 10.1021/acs.jctc.6b00075 or  PMID: 26967371)' />                            
                            </div>
                        </div>
                        <div className='form-group'>
                            <label className='control-label col-sm-2' htmlFor='email'>E-mail</label>
                            <div className='col-sm-10'>
                                <input type='text' className='form-control' id='email' placeholder='(optional) jon.snow@uni.ac.uk' />                            
                            </div>
                        </div>
                        <div className='form-group'>
                            <label className='control-label col-sm-2' htmlFor='annotation'>Annotation</label>
                            <textarea style={{width: '97.5%', marginLeft: '15px', marginTop: '35px'}} className='form-control' rows={7} id='annotation' placeholder='Tunnel 30.5Å. - Substrate channel\n\nTYR 23 A - Constriction region\nASN 1 B A part of NPA motif that orient the key central water molecule'></textarea>
                        </div>
                        <div className='input-group'>
                            <label className='input-group-btn'>
                                <span className='btn btn-default'>Select channels&hellip; <input type='file' style={{display: 'none'}} multiple /></span>
                            </label>
                            <input type='text' className='form-control' readOnly/>
                        </div><br/>
                        
                        
                        <button
                            className='btn btn-primary btn-block g-recaptcha'
                            data-sitekey='6LfccisUAAAAAH5uJXH3J-9KKc6ItSKS2luiXUFZ'
                            onClick={this.submitAnnotation}>
                            Submit
                        </button>
                    </form>

                <hr className='featurette-divider' style={{ margin: '50px 0' }} />

                <h1 className='text-center'>References</h1>   
                    <div className='tab-pane'>
                        <p>The ChannelsDB is build a over the top of the following services. Data annotations are taken from scientific literature, which is properly linked with the given entry.</p>
                        <dl className='publications-list'>
                            <dt>MOLE</dt>
                            <dd>
                                <p>Sehnal,D., Svobodová Vařeková,R., Berka,K., Pravda,L., Navrátilová,V., Banáš,P., Ionescu,C.-M., Otyepka,M. and Koča,J. (2013) <a href='https://dx.doi.org/10.1186/1758-2946-5-39' target='_blank'>MOLE 2.0: advanced approach for analysis of biomacromolecular channels</a>.
                                      J. Cheminform., 5, 39.</p>
                            </dd>
                            <dt>LiteMol suite</dt>
                            <dd>
                                <p><a href='https:/litemol.org' target='_blank'>LiteMol suite</a></p>
                            </dd>      
                            <dt>UniProt API</dt>
                            <dd>
                                <p>Nightingale,A., Antunes,R., Alpi,E., Bursteinas,B., Gonzales,L., Liu,W., Luo,J., Qi,G., Turner,E. and Martin,M. (2017) <a href='https://dx.doi.org/10.1093/nar/gkx237' target='_blank'>The Proteins API: accessing key integrated protein and genome information</a>.
                                      Nucleic Acids Res., 45, W539–W544.</p>
                            </dd>
                            <dt>Protein Data Bank in Europe</dt>
                            <dd>
                                <p>Velankar,S., van Ginkel,G., Alhroub,Y., Battle,G.M., Berrisford,J.M., Conroy,M.J., Dana,J.M., Gore,S.P., Gutmanas,A., Haslam,P., et al. (2016) <a href='https://dx.doi.org/10.1093/nar/gkv1047' target='_blank'>PDBe: improved accessibility of macromolecular structure data from PDB and EMDB</a>.
                                      Nucleic Acids Res., 44, D385–D395.</p>
                            </dd>                                                                              
                        </dl>
                    </div>
                             
            </div>;
        }
    }
}