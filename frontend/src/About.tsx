/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {
    export class About extends React.Component<{}, {}> {
        render() {
            return <div>
                <div className='row'>
                    <div className='col-md-8'>
                        <h2 className='featurette-heading'>Channels</h2>
                        <p>
                            Channels and pores are important regions of proteins and other biomacromolecules. They connect internal spaces of biomacromolecules with exterior enabling, e.g.,
                            substrates/product transport towards enzymes’ active sites, nascent synthetized proteins to leave ribosomal proteosynthetic center via ribosomal exit channel, etc. 
                            Pores represent a pathway passing through the whole biomacromolecular structure, typically facilitating transport of ions or molecules through cellular biomembranes.                    
                        </p>
                        <p>
                            Channel walls are made from surrounding amino acids constituting a specific microenvironment, which influence to a great extent specificity and selectivity of plethora
                            biologically important processes. Their constitution is especially important in narrowing sites sych as local minimas and bottlenecks.
                        </p>
                    </div>
                    <div className='col-md-4'>
                        <img className='featurette-image img-responsive center-block' src={'assets/img/channel_detail.png'} width='500' height='500' alt='Channel details' />
                    </div>
                </div>
                <div className='row'>
                    <div className='col-md-12'>
                        <h2 className='featurette-heading'>MOLE</h2>
                        <p>Lorem ipsum</p>
                    </div>
                </div>
                <div className='row'>
                    <div className='col-md-12'>
                        <h2 className='featurette-heading'>Physicochemical properties</h2>
                        <p>Lorem ipsum</p>
                    </div>
                </div>                                
            </div>;
        }
    }
}