"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TunnelShapeSimpleProvider = exports.TunnelShapeProvider = exports.TunnelDataProvider = exports.TunnelsDataProvider = void 0;
const objects_1 = require("../../../mol-plugin-state/objects");
const mol_state_1 = require("../../../mol-state");
const props_1 = require("./props");
const param_definition_1 = require("../../../mol-util/param-definition");
const mesh_1 = require("../../../mol-geo/geometry/mesh/mesh");
const mol_task_1 = require("../../../mol-task");
const color_1 = require("../../../mol-util/color");
const algorithm_1 = require("./algorithm");
const Transform = mol_state_1.StateTransformer.builderFactory("sb-ncbr-tunnels");
exports.TunnelsDataProvider = Transform({
    name: 'tunnels-from-data',
    display: { name: 'Channels' },
    from: objects_1.PluginStateObject.Data.String,
    to: props_1.TunnelStateObject,
    params: {
        kind: param_definition_1.ParamDefinition.MappedStatic('raw', {
            raw: param_definition_1.ParamDefinition.EmptyGroup(),
            trajectory: param_definition_1.ParamDefinition.Group({
                index: param_definition_1.ParamDefinition.Numeric(0)
            })
        }),
        channel_index: param_definition_1.ParamDefinition.Numeric(0),
        channel: param_definition_1.ParamDefinition.Select('CSATunnels_MOLE', param_definition_1.ParamDefinition.arrayToOptions([
            'CSATunnels_MOLE',
            'CSATunnels_Caver',
            'ReviewedChannels_MOLE',
            'ReviewedChannels_Caver',
            'CofactorTunnels_MOLE',
            'CofactorTunnels_Caver',
            'TransmembranePores_MOLE',
            'TransmembranePores_Caver',
            'ProcognateTunnels_MOLE',
            'ProcognateTunnels_Caver',
            'AlphaFillTunnels_MOLE',
            'AlphaFillTunnels_Caver'
        ]))
    }
})({
    apply({ a, params, cache }) {
        const data = JSON.parse(a.data);
        cache.Channels = data.Channels;
        const channel = data.Channels[params.channel][params.channel_index];
        if (!channel) {
            return new props_1.TunnelStateObject({
                tunnel: { data: [], type: 'Empty', id: '' }
            }, { label: "Channel settings" });
        }
        return new props_1.TunnelStateObject({
            tunnel: { data: channel.Profile, type: channel.Type, id: channel.Id }
        }, { label: "Channel settings" });
    },
    update({ a, b, newParams, cache }) {
        const channel = cache.Channels[newParams.channel][newParams.channel_index];
        if (!channel) {
            b.data.tunnel.type = 'Empty';
            b.data.tunnel.id = "";
            b.data.tunnel.data = [];
            return mol_state_1.StateTransformer.UpdateResult.Updated;
        }
        b.data.tunnel.type = channel.Type;
        b.data.tunnel.id = channel.Id;
        b.data.tunnel.data = channel.Profile;
        return mol_state_1.StateTransformer.UpdateResult.Updated;
    }
});
exports.TunnelDataProvider = Transform({
    name: 'tunnel-from-data',
    display: { name: 'Channel' },
    from: objects_1.PluginStateObject.Data.String,
    to: props_1.TunnelStateObject,
    params: {
        kind: param_definition_1.ParamDefinition.MappedStatic('raw', {
            raw: param_definition_1.ParamDefinition.EmptyGroup(),
            trajectory: param_definition_1.ParamDefinition.Group({
                index: param_definition_1.ParamDefinition.Numeric(0)
            })
        })
    }
})({
    apply({ a, params }) {
        const data = JSON.parse(a.data);
        return new props_1.TunnelStateObject({
            tunnel: { data: data.Profile, type: data.Type, id: data.Id }
        }, { label: "Channel settings" });
    }
});
exports.TunnelShapeProvider = Transform({
    name: 'tunnel-shape',
    display: { name: 'Channel' },
    from: props_1.TunnelStateObject,
    to: objects_1.PluginStateObject.Shape.Provider,
    params: {
        webgl: param_definition_1.ParamDefinition.Value(null),
        colorTheme: param_definition_1.ParamDefinition.Color((0, color_1.Color)(0xff0000)),
        visual: param_definition_1.ParamDefinition.MappedStatic('mesh', {
            mesh: param_definition_1.ParamDefinition.Group({ resolution: param_definition_1.ParamDefinition.Numeric(2) }),
            spheres: param_definition_1.ParamDefinition.Group({ resolution: param_definition_1.ParamDefinition.Numeric(2) })
        }),
    },
})({
    apply({ a, params }) {
        return mol_task_1.Task.create('Tunnel Shape Representation', async (ctx) => {
            return new objects_1.PluginStateObject.Shape.Provider({
                label: 'Channel',
                data: { tunnel: a.data.tunnel, params },
                params: mesh_1.Mesh.Params,
                geometryUtils: mesh_1.Mesh.Utils,
                getShape: (_, data) => data.params.visual.name === 'mesh'
                    ? (0, algorithm_1.createTunnelShape)(data.tunnel, data.params.webgl, data.params.visual.params.resolution, data.params.colorTheme)
                    : (0, algorithm_1.createSpheresShape)(data.tunnel, data.params.webgl, data.params.visual.params.resolution, data.params.colorTheme)
            }, { label: `${a.data.tunnel.type} ${a.data.tunnel.id}` });
        });
    },
});
exports.TunnelShapeSimpleProvider = Transform({
    name: 'tunnel-shape',
    display: { name: 'Channel' },
    from: objects_1.PluginStateObject.Root,
    to: objects_1.PluginStateObject.Shape.Provider,
    params: {
        data: param_definition_1.ParamDefinition.Value({ data: [], type: '', id: '' }),
        webgl: param_definition_1.ParamDefinition.Value(null),
        colorTheme: param_definition_1.ParamDefinition.Color((0, color_1.Color)(0xff0000)),
        visual: param_definition_1.ParamDefinition.MappedStatic('mesh', {
            mesh: param_definition_1.ParamDefinition.Group({ resolution: param_definition_1.ParamDefinition.Numeric(2) }),
            spheres: param_definition_1.ParamDefinition.Group({ resolution: param_definition_1.ParamDefinition.Numeric(2) })
        }),
    },
})({
    apply({ params }) {
        return mol_task_1.Task.create('Tunnel Shape Representation', async (ctx) => {
            return new objects_1.PluginStateObject.Shape.Provider({
                label: 'Channel',
                data: { params },
                params: mesh_1.Mesh.Params,
                geometryUtils: mesh_1.Mesh.Utils,
                getShape: (_, data) => data.params.visual.name === 'mesh'
                    ? (0, algorithm_1.createTunnelShape)(data.data, data.colorTheme, data.params.visual.params.resolution, data.webgl)
                    : (0, algorithm_1.createSpheresShape)(data.data, data.colorTheme, data.params.visual.params.resolution, data.webgl)
            }, { label: `${params.data.type} ${params.data.id}` });
        });
    },
});
