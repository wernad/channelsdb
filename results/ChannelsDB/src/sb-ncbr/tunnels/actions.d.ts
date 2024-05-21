/**
 * Copyright (c) 2024 mol* contributors, licensed under MIT, See LICENSE file for more info.
 *
 * @author Dušan Veľký <dvelky@mail.muni.cz>
 */
import { PluginStateObject } from 'molstar/lib/mol-plugin-state/objects';
import { StateAction } from 'molstar/lib/mol-state';
import { ParamDefinition as PD } from 'molstar/lib/mol-util/param-definition';
export declare const TunnelDownloadServer: {
    channelsdb: PD.Group<PD.Normalize<unknown>>;
};
export declare const DownloadTunnels: StateAction<PluginStateObject.Root, void, PD.Normalize<{
    source: PD.NamedParams<PD.Normalize<{
        url: any;
    }>, "url"> | PD.NamedParams<PD.Normalize<{
        provider: any;
    }>, "alphafolddb"> | PD.NamedParams<PD.Normalize<{
        provider: any;
    }>, "pdb">;
}>>;
