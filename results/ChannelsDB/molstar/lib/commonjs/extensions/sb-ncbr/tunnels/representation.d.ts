import { PluginStateObject } from "../../../mol-plugin-state/objects";
import { StateTransformer } from "../../../mol-state";
import { TunnelStateObject, Tunnel } from "./props";
import { ParamDefinition as PD } from "../../../mol-util/param-definition";
import { WebGLContext } from "../../../mol-gl/webgl/context";
import { Color } from "../../../mol-util/color";
export declare const TunnelsDataProvider: StateTransformer<PluginStateObject.Data.String, TunnelStateObject, PD.Normalize<{
    kind: PD.NamedParams<PD.Normalize<unknown>, "raw"> | PD.NamedParams<PD.Normalize<{
        index: any;
    }>, "trajectory">;
    channel_index: number;
    channel: string;
}>>;
export declare const TunnelDataProvider: StateTransformer<PluginStateObject.Data.String, TunnelStateObject, PD.Normalize<{
    kind: PD.NamedParams<PD.Normalize<unknown>, "raw"> | PD.NamedParams<PD.Normalize<{
        index: any;
    }>, "trajectory">;
}>>;
export declare const TunnelShapeProvider: StateTransformer<TunnelStateObject, PluginStateObject.Shape.Provider, PD.Normalize<{
    webgl: WebGLContext | null;
    colorTheme: Color;
    visual: PD.NamedParams<PD.Normalize<{
        resolution: any;
    }>, "mesh"> | PD.NamedParams<PD.Normalize<{
        resolution: any;
    }>, "spheres">;
}>>;
export declare const TunnelShapeSimpleProvider: StateTransformer<PluginStateObject.Root, PluginStateObject.Shape.Provider, PD.Normalize<{
    data: Tunnel;
    webgl: WebGLContext | null;
    colorTheme: Color;
    visual: PD.NamedParams<PD.Normalize<{
        resolution: any;
    }>, "mesh"> | PD.NamedParams<PD.Normalize<{
        resolution: any;
    }>, "spheres">;
}>>;
