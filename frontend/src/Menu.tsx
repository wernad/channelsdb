/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {
    export class Menu extends React.Component<{}, {}> {
        render() {
            return <nav className='navbar navbar-default'>
                <div className='container-fluid'>
                    <div className='navbar-header'>
                        <a href='index.html'><img height='50' style={{margin: '10px 0'}} src={'assets/img/channelsdb_logo.png'}/></a>
                    </div>
                    <div id='navbar' className='navbar-collapse collapse'>
                        <ul className='nav navbar-nav navbar-right'>
                            <li style={{marginTop: '12px', fontSize: '120%', fontWeight: 'bold'}}><a href='index.html'>Search</a></li>
                            <li style={{marginTop: '12px', fontSize: '120%', fontWeight: 'bold'}}><a href='methods.html'>Methods</a></li>
                            <li style={{marginTop: '12px', fontSize: '120%', fontWeight: 'bold'}}><a href='documentation.html'>Documentation</a></li>                            
                            <li style={{marginTop: '12px', fontSize: '120%', fontWeight: 'bold'}}><a href='https://mole.upol.cz' target='_blank'>MOLE</a></li>                            
                            <li style={{marginTop: '12px', fontSize: '120%', fontWeight: 'bold'}}><a href='contribute.html'>Contribute</a></li>
                            <li style={{marginTop: '12px', fontSize: '120%', fontWeight: 'bold'}}><a href='about.html'>About</a></li>
                            {/*<li><a href='#'>Contribute</a></li>*/}
                        </ul>
                    </div>
                </div>
            </nav>;
        }
    }
}