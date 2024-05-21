import { PluginConfigItem } from 'molstar/lib/mol-plugin/config';
import { PluginContext } from 'molstar/lib/mol-plugin/context';
import { ParamDefinition as PD } from 'molstar/lib/mol-util/param-definition';
export declare namespace TunnelsData {
    const DefaultServerUrl = "https://channelsdb2.biodata.ceitec.cz/api";
    const DefaultServerType = "pdb";
}
export declare const TunnelsDataParams: {
    serverType: PD.Select<"pdb">;
    serverUrl: PD.Text<string>;
};
export type TunnelsDataParams = typeof TunnelsDataParams;
export declare const TunnelsServerConfig: {
    DefaultServerUrl: PluginConfigItem<string>;
    DefaultServerType: PluginConfigItem<"pdb">;
};
export declare function getTunnelsConfig(plugin: PluginContext): {
    [key in keyof typeof TunnelsServerConfig]: NonNullable<typeof TunnelsServerConfig[key]['defaultValue']>;
};
