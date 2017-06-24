/*
 * Copyright (c) 2017 David Sehnal, licensed under Apache 2.0, See LICENSE file for more info.
 */

namespace ChannelsDB {
    export class Menu extends React.Component<{}, {}> {
        render() {
            return <nav className='navbar navbar-default'>
                <div className='container-fluid'>
                    <div className='navbar-header'>
                        <a className='navbar-brand' href='index.html' style={{ fontWeight: 'bold' }}>ChannelsDB</a>
                    </div>
                    <div id='navbar' className='navbar-collapse collapse'>
                        <ul className='nav navbar-nav navbar-right'>
                            <li><a href='methods.html'>Methods</a></li>
                            <li><a href='documentation.html'>Documentation</a></li>
                            <li><a href='http://mole.upol.cz' target='_blank'>MOLE</a></li>                            
                            {/*<li><a href='#'>Contribute</a></li>*/}
                        </ul>
                    </div>
                </div>
            </nav>;
        }
    }
}