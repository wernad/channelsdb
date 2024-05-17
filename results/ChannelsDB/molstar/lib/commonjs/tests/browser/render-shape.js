"use strict";
/**
 * Copyright (c) 2019 mol* contributors, licensed under MIT, See LICENSE file for more info.
 *
 * @author Alexander Rose <alexander.rose@weirdbyte.de>
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.init = void 0;
require("./index.html");
const util_1 = require("../../mol-canvas3d/util");
const representation_1 = require("../../mol-repr/representation");
const canvas3d_1 = require("../../mol-canvas3d/canvas3d");
const label_1 = require("../../mol-theme/label");
const marker_action_1 = require("../../mol-util/marker-action");
const loci_1 = require("../../mol-model/loci");
const mol_task_1 = require("../../mol-task");
const mesh_1 = require("../../mol-geo/geometry/mesh/mesh");
const mesh_builder_1 = require("../../mol-geo/geometry/mesh/mesh-builder");
const linear_algebra_1 = require("../../mol-math/linear-algebra");
const sphere_1 = require("../../mol-geo/primitive/sphere");
const names_1 = require("../../mol-util/color/names");
const shape_1 = require("../../mol-model/shape");
const representation_2 = require("../../mol-repr/shape/representation");
const assets_1 = require("../../mol-util/assets");
const parent = document.getElementById('app');
parent.style.width = '100%';
parent.style.height = '100%';
const canvas = document.createElement('canvas');
parent.appendChild(canvas);
(0, util_1.resizeCanvas)(canvas, parent);
const assetManager = new assets_1.AssetManager();
const info = document.createElement('div');
info.style.position = 'absolute';
info.style.fontFamily = 'sans-serif';
info.style.fontSize = '24pt';
info.style.bottom = '20px';
info.style.right = '20px';
info.style.color = 'white';
parent.appendChild(info);
let prevReprLoci = representation_1.Representation.Loci.Empty;
const canvas3d = canvas3d_1.Canvas3D.create(canvas3d_1.Canvas3DContext.fromCanvas(canvas, assetManager));
canvas3d.animate();
canvas3d.input.move.subscribe(({ x, y }) => {
    var _a;
    const pickingId = (_a = canvas3d.identify(x, y)) === null || _a === void 0 ? void 0 : _a.id;
    let label = '';
    if (pickingId) {
        const reprLoci = canvas3d.getLoci(pickingId);
        label = (0, label_1.lociLabel)(reprLoci.loci);
        if (!representation_1.Representation.Loci.areEqual(prevReprLoci, reprLoci)) {
            canvas3d.mark(prevReprLoci, marker_action_1.MarkerAction.RemoveHighlight);
            canvas3d.mark(reprLoci, marker_action_1.MarkerAction.Highlight);
            prevReprLoci = reprLoci;
        }
    }
    else {
        canvas3d.mark({ loci: loci_1.EveryLoci }, marker_action_1.MarkerAction.RemoveHighlight);
        prevReprLoci = representation_1.Representation.Loci.Empty;
    }
    info.innerText = label;
});
/**
 * Create a mesh of spheres at given centers
 * - asynchronous (using async/await)
 * - progress tracking (via `ctx.update`)
 * - re-use storage from an existing mesh if given
 */
async function getSphereMesh(ctx, centers, mesh) {
    const builderState = mesh_builder_1.MeshBuilder.createState(centers.length * 128, centers.length * 128 / 2, mesh);
    const t = linear_algebra_1.Mat4.identity();
    const v = linear_algebra_1.Vec3.zero();
    const sphere = (0, sphere_1.Sphere)(3);
    builderState.currentGroup = 0;
    for (let i = 0, il = centers.length / 3; i < il; ++i) {
        // for production, calls to update should be guarded by `if (ctx.shouldUpdate)`
        await ctx.update({ current: i, max: il, message: `adding sphere ${i}` });
        builderState.currentGroup = i;
        linear_algebra_1.Mat4.setTranslation(t, linear_algebra_1.Vec3.fromArray(v, centers, i * 3));
        mesh_builder_1.MeshBuilder.addPrimitive(builderState, t, sphere);
    }
    return mesh_builder_1.MeshBuilder.getMesh(builderState);
}
const myData = {
    centers: [0, 0, 0, 0, 3, 0, 1, 0, 4],
    colors: [names_1.ColorNames.tomato, names_1.ColorNames.springgreen, names_1.ColorNames.springgreen],
    labels: ['Sphere 0, Instance A', 'Sphere 1, Instance A', 'Sphere 0, Instance B', 'Sphere 1, Instance B'],
    transforms: [linear_algebra_1.Mat4.identity(), linear_algebra_1.Mat4.fromTranslation(linear_algebra_1.Mat4.zero(), linear_algebra_1.Vec3.create(3, 0, 0))]
};
/**
 * Get shape from `MyData` object
 */
async function getShape(ctx, data, props, shape) {
    await ctx.update('async creation of shape from  myData');
    const { centers, colors, labels, transforms } = data;
    const mesh = await getSphereMesh(ctx, centers, shape && shape.geometry);
    const groupCount = centers.length / 3;
    return shape_1.Shape.create('test', data, mesh, (groupId) => colors[groupId], // color: per group, same for instances
    () => 1, // size: constant
    (groupId, instanceId) => labels[instanceId * groupCount + groupId], // label: per group and instance
    transforms);
}
// Init ShapeRepresentation container
const repr = (0, representation_2.ShapeRepresentation)(getShape, mesh_1.Mesh.Utils);
async function init() {
    // Create shape from myData and add to canvas3d
    await repr.createOrUpdate({}, myData).run((p) => console.log(mol_task_1.Progress.format(p)));
    console.log('shape', repr);
    canvas3d.add(repr);
    canvas3d.requestCameraReset();
    // Change color after 1s
    setTimeout(async () => {
        myData.colors[0] = names_1.ColorNames.darkmagenta;
        // Calling `createOrUpdate` with `data` will trigger color and transform update
        await repr.createOrUpdate({}, myData).run();
    }, 1000);
}
exports.init = init;
init();
