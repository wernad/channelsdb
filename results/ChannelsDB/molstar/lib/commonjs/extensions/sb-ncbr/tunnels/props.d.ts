import { PluginStateObject } from "../../../mol-plugin-state/objects";
import { ParamDefinition as PD } from "../../../mol-util/param-definition";
export interface Profile {
    Charge: number;
    Radius: number;
    FreeRadius: number;
    T: number;
    Distance: number;
    X: number;
    Y: number;
    Z: number;
}
export interface Channels {
    "CSATunnels_MOLE": [];
    "CSATunnels_Caver": [];
    "ReviewedChannels_MOLE": [];
    "ReviewedChannels_Caver": [];
    "CofactorTunnels_MOLE": [];
    "CofactorTunnels_Caver": [];
    "TransmembranePores_MOLE": [];
    "TransmembranePores_Caver": [];
    "ProcognateTunnels_MOLE": [];
    "ProcognateTunnels_Caver": [];
    "AlphaFillTunnels_MOLE": [];
    "AlphaFillTunnels_Caver": [];
}
export interface ChannelsCache {
    Channels: Channels;
}
export interface Tunnel {
    data: Profile[];
    type: string;
    id: number | string;
}
export declare const TunnelParams: {
    data: PD.Value<any[]>;
    visual: PD.Mapped<PD.NamedParams<PD.Normalize<{
        resolution: number;
    }>, "mesh"> | PD.NamedParams<PD.Normalize<{
        resolution: number;
    }>, "sphere">>;
};
declare const TunnelStateObject_base: {
    new (data: {
        tunnel: Tunnel;
    }, props?: {
        label: string;
        description?: string | undefined;
    } | undefined): {
        id: import("../../../mol-util").UUID;
        type: PluginStateObject.TypeInfo;
        label: string;
        description?: string | undefined;
        data: {
            tunnel: Tunnel;
        };
    };
    type: PluginStateObject.TypeInfo;
    is(obj?: import("../../../mol-state").StateObject<any, import("../../../mol-state").StateObject.Type<any>> | undefined): obj is import("../../../mol-state").StateObject<{
        tunnel: Tunnel;
    }, PluginStateObject.TypeInfo>;
};
export declare class TunnelStateObject extends TunnelStateObject_base {
}
export {};
