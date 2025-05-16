/**
 * Copyright (c) 2024 channelsdb contributors, licensed under Apache 2.0, See LICENSE file for more info.
 *
 * @author Dušan Veľký <dvelky@mail.muni.cz>
 */
import type { Context } from "../Context";
import { Plugin } from "molstar/lib/mol-plugin-ui/plugin";
import { GlobalRouter } from "../SimpleRouter";
import { IDType } from "../DataInterface";
import React from "react";
require("molstar/lib/mol-plugin-ui/skin/dark.scss");

export class Viewer extends React.Component<{ context: Context }> {

    render() {
        let pid = GlobalRouter.getCurrentPid();
        const pidType = GlobalRouter.getCurrentPidType();
        this.props.context.canvas.setBgColor({ r: 0, g: 0, b: 0 })

        if (pidType === IDType.PdbOld) {
            this.props.context.load(`https://models.rcsb.org/${pid}.bcif`, true)
            // this.props.context.load(`https://www.ebi.ac.uk/pdbe/entry-files/download/${pid}.bcif`)
        } else if (pidType === IDType.PdbNew) {
            const oldFormat = GlobalRouter.tryGetOldPdbId();
            this.props.context.load(`https://models.rcsb.org/${oldFormat}.bcif`, true)
        } else {
            this.props.context.load(`https://alphafill.eu/v1/aff/${pid.toLocaleUpperCase()}`, false);
        }

        return <Plugin plugin={this.props.context.plugin} />;
    }
}
