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
                                    <td>Solvent tunnel</td>
                                    <td>Channel transporting water molecules, which are consumed/egressed during a chemical reaction</td>
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
                                    <td>Water channel</td>
                                    <td>Transports water molecules; mainly found in aquaporins.</td>
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

                <div className='row'>
                    <h2 className='featurette-heading'>MOLE settings</h2>
                    <p style={justify}>Throughout the ChannelsDB the folowing settings of the MOLE algorithm has been used for the CSA and cofactor tunnels. For reviewed channels,
                        each calculation has been independently adjusted, in order to extract deemed channel.</p>
                    <div className='row table-responsive col-md-4 col-md-offset-1'>
                        <h2 className='featurette-heading'>CSA tunnels</h2>
                        <table className='table table-condensed active'>
                            <thead>
                                <tr>
                                    <th>Parameter</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><i>ProbeRadius</i></td>
                                    <td>5.0</td>
                                </tr>
                                <tr>
                                    <td><i>InteriorThreshold</i></td>
                                    <td>1.1</td>
                                </tr>
                                <tr>
                                    <td><i>MinTunnelLength</i></td>
                                    <td>15.0</td>
                                </tr>
                                <tr>
                                    <td><i>BottleneckRadius</i></td>
                                    <td>1.25</td>
                                </tr>
                                <tr>
                                    <td><i>BottleneckTolerance</i></td>
                                    <td>3.0</td>
                                </tr>
                                <tr>
                                    <td><i>MaxTunnelSimilarity</i></td>
                                    <td>0.7</td>
                                </tr>                                                                                                
                                <tr>
                                    <td><i>NonActiveParts</i></td>
                                    <td data-toggle='tooltip' title='HetResidues().Filter(lambda m: m.IsNotConnectedTo(AminoAcids()))'>Query</td>
                                </tr>                                                                                                
                            </tbody>
                        </table>
                    </div>

                    <div className='row table-responsive col-md-4 col-md-push-2'>
                        <h2 className='featurette-heading'>Cofactor tunnels</h2>
                        <table className='table table-condensed active'>
                            <thead>
                                <tr>
                                    <th>Parameter</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><i>ProbeRadius</i></td>
                                    <td>5.0</td>
                                </tr>
                                <tr>
                                    <td><i>InteriorThreshold</i></td>
                                    <td>1.4</td>
                                </tr>
                                <tr>
                                    <td><i>IgnoreHetResidues</i></td>
                                    <td>True</td>
                                </tr>
                                <tr>
                                    <td><i>MinTunnelLength</i></td>
                                    <td>15.0</td>
                                </tr>
                                <tr>
                                    <td><i>BottleneckRadius</i></td>
                                    <td>1.25</td>
                                </tr>
                                <tr>
                                    <td><i>BottleneckTolerance</i></td>
                                    <td>1.0</td>
                                </tr>
                                <tr>
                                    <td><i>MaxTunnelSimilarity</i></td>
                                    <td>0.7</td>
                                </tr>                                                                                                
                                <tr>
                                    <td><i>NonActiveParts</i></td>
                                    <td data-toggle='tooltip' title='Various queries e.g. Atoms("Fe").Inside(Residues("HEM", "HEC", "HEA"))'>Query</td>
                                </tr>                                                                                                
                            </tbody>
                        </table>
                    </div>
                </div>

                <hr className='featurette-divider' style={{ margin: '50px 0' }} />

                <div className='row'>
                        <h2 className='featurette-heading'>Cofactors list</h2>
                        <p>Following well-known cofactors, which are often burried within a protein structure have been selected for channel prediction. </p>
                        <div className='row table-responsive col-md-8 col-md-offset-2'>
                            <table className='table table-condensed active'>
                            <thead>
                            <tr>
                                <th>Group</th>
                                <th>Origin</th>
                                <th>Ligand list</th>                                
                            </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Hems</td>
                                    <td>Fe (<i>type_symbol</i>)</td>
                                    <td><i>HEA, HEM, HEC</i></td>
                                </tr>
                                <tr>
                                    <td>Flavins</td>
                                    <td>N5 (<i>auth_atom_id</i>)</td>
                                    <td><i>FAD, FMN</i></td>
                                </tr>
                                <tr>
                                    <td>Nicotinadenins</td>
                                    <td>N1N (<i>auth_atom_id</i>)</td>
                                    <td><i>NAD, NAP, NDP, NAI</i></td>
                                </tr>
                                <tr>
                                    <td>Nucleotides</td>
                                    <td>PA atom (<i>auth_atom_id</i>)</td>
                                    <td><i>ATP, CTP, UTP, GTP, TTP, ADP, CDP, UDP, GDP, TDP, AMP, CMP, ANP</i></td>
                                </tr>                               
                                <tr>
                                    <td>Vitamin B2</td>
                                    <td>N5 (<i>auth_atom_id</i>)</td>
                                    <td><i>RBF</i></td>
                                </tr>
                                <tr>
                                    <td>Vitamin B6</td>
                                    <td>C4A (<i>auth_atom_id</i>)</td>
                                    <td><i>PLP</i></td>
                                </tr>
                                <tr>
                                    <td>Vitamin B12</td>
                                    <td>CO (<i>auth_atom_id</i>)</td>
                                    <td><i>B12</i></td>
                                </tr>         
                                <tr>
                                    <td>Biotin</td>
                                    <td>C3 (<i>auth_atom_id</i>)</td>
                                    <td><i>BTN</i></td>
                                </tr>                                                                
                                <tr>
                                    <td>Coenzym</td>
                                    <td>S1P (<i>auth_atom_id</i>)</td>
                                    <td><i>COA, ACO</i></td>
                                </tr>                                
                                <tr>
                                    <td>Glutathione</td>
                                    <td>SG2 (<i>auth_atom_id</i>)</td>
                                    <td><i>GSH, GDS</i></td>
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
                                 Right next to the visualization pane is a list of all channels identified for the particular PDB entry displayed. All channels are grouped to respective categories.
                              </li>
                              <li>
                                Directly below the visualization pane you can find an interactive visualization of a channel profile. All the physicochemical properties are mapped on the
                                channel profile. User can select deemed type of property to visualize, change the radius being mesured to the closest atom or to the backbone. ON the top of that to a publication quality image is available for export as well.
                              </li>
                              <li>
                                  Next to the 2D channel visualization is a list with details for individual regions of a channel so called layers. Additional level of information is provided
                                  as a residue level annotations with the respective reference.
                             </li>
                             <li> Protein annotatios from the UniProt resource.</li>
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