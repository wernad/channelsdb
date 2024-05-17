"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TunnelStateObject = exports.TunnelParams = void 0;
const objects_1 = require("../../../mol-plugin-state/objects");
const param_definition_1 = require("../../../mol-util/param-definition");
exports.TunnelParams = {
    data: param_definition_1.ParamDefinition.Value([], { isHidden: true }),
    visual: param_definition_1.ParamDefinition.MappedStatic('mesh', {
        mesh: param_definition_1.ParamDefinition.Group({
            resolution: param_definition_1.ParamDefinition.Numeric(2),
        }),
        sphere: param_definition_1.ParamDefinition.Group({
            resolution: param_definition_1.ParamDefinition.Numeric(2)
        })
    })
};
class TunnelStateObject extends objects_1.PluginStateObject.Create({ name: 'Tunnel Entry', typeClass: 'Data' }) {
}
exports.TunnelStateObject = TunnelStateObject;
