/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {
    export class Documentation extends React.Component<{}, {}> {
        render() {
            let justify = {
                textAlign: 'justify',
                textJustify: 'inter-word',
            };

            return <div style={{ margin: '60px 0 0 20px' }}>

                <h1 className='text-center'>Documentation</h1>                

                <div className='row'>
                    <div className='col-md-8'>
                        <h2 className='featurette-heading'>Database content</h2>
                        <p>
                            <b>The entire database is composed out of the following content:</b>
                                <ul>
                                    <li>Hand currated channel annotations from literature extracted entries</li>
                                    <li>Ligad-accessible tunnels to the catalytic sites annotated in the <a target='_blank' href='http://www.ebi.ac.uk/thornton-srv/databases/CSA/'>Catalytic Site Atlas</a></li>
                                    <li>Pores in transmembrane proteins enabling flow of ions and small molecules across the lipid bilayer for proteins deposited in the <a target='_blank' href='http://opm.phar.umich.edu/' >OPM</a> database</li>
                                    <li>Product/substrate tunnels leading towards the well-known enzyme cofactors such as <abbr className='abbr initialism' title='HEME (Protoporhpyrin IX containing Fe)'>HEM</abbr> or <abbr className='abbr initialism' title='Flavin-adenine dinucleotide'>FAD</abbr></li>
                                </ul>
                            All the channels have been extracted from biological assemblies as identified by the Protein Data Bank in Europe.
                        </p>
                    </div>
                    <div className='col-md-4'>
                        <img className='featurette-image img-responsive center-block' src={'assets/img/pretty_channel.png'} width='500' height='500' alt='Channel details' />
                    </div>
                </div>

                <hr className='featurette-divider' style={{ margin: '50px 0' }} />

                <div className='row'>
                        <h2 className='featurette-heading'>Channel nomenclature</h2>
                        <p>Unless the channel has been given a particular name in literature, which is the case e.g. for a group of <a href='https://dx/doi.org/10.1016/j.bbagen.2006.07.005' target='_blank'>cytorchome P450s</a>, names are given to according to 
                            the following controlled vocabulary:</p>
                        <div className='row table-responsive col-md-8 col-md-offset-2'>
                            <table className='table table-condensed active'>
                            <thead>
                            <tr>
                                <th>Name</th>
                                <th>Description</th>
                            </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Channel</td>
                                    <td>Generic term for any ligand transporting pathway</td>
                                </tr>
                                <tr>
                                    <td>Tunnel</td>
                                    <td>Generic term for a ligand transporting pathway towards the enzyme active site</td>
                                </tr>
                                <tr>
                                    <td>Pore</td>
                                    <td>Generic term for a channel spanning across a lipid bilayer</td>
                                </tr>
                                <tr>
                                    <td>Solvent channel</td>
                                    <td>Channel transporting water molecules, which are consumed/egressed during a chemical reaction</td>
                                </tr>
                                <tr>
                                    <td>Water channel</td>
                                    <td>Transports water molecules; mainly found in aquaporins.</td>
                                </tr>
                                <tr>
                                    <td>Substrate tunnel</td>
                                    <td>Channel transporting various chemical species consumed in a chemical reaction</td>
                                </tr>
                                <tr>
                                    <td>Product tunnel</td>
                                    <td>Transports chemical species that are an outcome of chemical reaction</td>
                                </tr>
                                <tr>
                                    <td>Ion channel</td>
                                    <td>Provides pathways for ion and other charged chemical species to pass through lipid bilayer</td>
                                </tr>                          
                                <tr>  
                                    <td>Hydrophobic channel</td>
                                    <td>Provides pathways for apolar chemical species to pass through lipid bilayer</td>
                                </tr>
                            </tbody>                        
                        </table>    
                    </div>
                </div>

                <hr className='featurette-divider' style={{ margin: '50px 0' }} />                

                <div className='row featurette'>
                        <h2 className='featurette-heading'>Results interpretation</h2>
                        <div className='col-md-5'>
                        <p style={justify}>The results page is separated into 5 different sections. All of them are interactive, so play around!</p>
                          <ol>
                              <li>
                                The main part contains molecule visualization using LiteMol. The documentation how to change visual representation of the results
                                is available in the <a href='https://webchem.ncbr.muni.cz/Wiki/LiteMol:UserManual' target='_blank'>LiteMol documentation</a>.
                              </li>
                              <li>
                                 Right next to the visualization pane a list of all channels identified for the particular PDB entry is displayed. Channels are grouped to the respective categories
                              </li>
                              <li>
                                Directly below the visualization pane you can fin an interactive visualilization of a channel profile. All the physicochemical properties are mapped on the
                                channel profile, so the user can select deemed type of visualization. Export to a publication quality image is available as well.
                              </li>
                              <li>
                                  Next to the 2D channel visualization is a panel with details for individual regions of the channel so called layers. Additional level of information is provided
                                  as a residue level annotations with respective reference.
                             </li>
                             <li> Protein annotatio from the UniProt resource</li>
                          </ol>
                            
                        </div>                    
                    <div className='col-md-7'>
                        <img className='featurette-image img-responsive center-block' src={'assets/img/web-fig1.png'} width='500' height='500' alt='Result window detail' />
                    </div>                    
                </div>

                <div style={{ margin: '50px 0' }} className='row featurette col-md-12'>
                        <img className='featurette-image img-responsive center-block' src={'assets/img/web-fig2.png'} width='800' alt='2D detailed channel view' />
                </div>  
            </div>;
        }
    }
}