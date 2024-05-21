/**
 * Copyright (c) 2024 channelsdb contributors, licensed under Apache 2.0, See LICENSE file for more info.
 *
 * @author Dušan Veľký <dvelky@mail.muni.cz>
 */
import React from "react";
import DownloadReport from "../DownloadReport/UI";
import PdbIdSign from "../PdbIdSign/UI";

export class Controls extends React.Component<{}, {}> {
    render() {
        return <div className="channelsdb-controls">
            <div className="home-button" title="Home"><a href="/"><span className="glyphicon glyphicon-home" /></a></div>
            <PdbIdSign />
            <DownloadReport />
        </div>
    }
}