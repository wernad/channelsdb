"use strict";
/**
 * Copyright (c) 2023 mol* contributors, licensed under MIT, See LICENSE file for more info.
 *
 * @author Adam Midlik <midlik@gmail.com>
 */
Object.defineProperty(exports, "__esModule", { value: true });
const tree_schema_1 = require("../../generic/tree-schema");
const mvs_builder_1 = require("../mvs-builder");
const mvs_tree_1 = require("../mvs-tree");
describe('mvs-builder', () => {
    it('mvs-builder demo works', async () => {
        const mvsData = (0, mvs_builder_1.builderDemo)();
        expect(typeof mvsData.metadata.version).toEqual('string');
        expect(typeof mvsData.metadata.timestamp).toEqual('string');
        expect((0, tree_schema_1.treeValidationIssues)(mvs_tree_1.MVSTreeSchema, mvsData.root)).toEqual(undefined);
    });
});
