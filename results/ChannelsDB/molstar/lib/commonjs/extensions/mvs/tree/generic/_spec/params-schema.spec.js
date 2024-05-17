"use strict";
/**
 * Copyright (c) 2023 mol* contributors, licensed under MIT, See LICENSE file for more info.
 *
 * @author Adam Midlik <midlik@gmail.com>
 */
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const iots = tslib_1.__importStar(require("io-ts"));
const params_schema_1 = require("../params-schema");
describe('fieldValidationIssues', () => {
    it('fieldValidationIssues string', async () => {
        const stringField = (0, params_schema_1.RequiredField)(iots.string);
        expect((0, params_schema_1.fieldValidationIssues)(stringField, 'hello')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(stringField, '')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(stringField, 5)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(stringField, null)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(stringField, undefined)).toBeTruthy();
    });
    it('fieldValidationIssues string choice', async () => {
        const colorParam = (0, params_schema_1.RequiredField)((0, params_schema_1.literal)('red', 'green', 'blue', 'yellow'));
        expect((0, params_schema_1.fieldValidationIssues)(colorParam, 'red')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(colorParam, 'green')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(colorParam, 'blue')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(colorParam, 'yellow')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(colorParam, 'banana')).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(colorParam, 5)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(colorParam, null)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(colorParam, undefined)).toBeTruthy();
    });
    it('fieldValidationIssues number choice', async () => {
        const numberParam = (0, params_schema_1.RequiredField)((0, params_schema_1.literal)(1, 2, 3, 4));
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, 1)).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, 2)).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, 3)).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, 4)).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, 5)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, '1')).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, null)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, undefined)).toBeTruthy();
    });
    it('fieldValidationIssues int', async () => {
        const numberParam = (0, params_schema_1.RequiredField)(iots.Integer);
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, 1)).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, 0)).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, 0.5)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, '1')).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, null)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(numberParam, undefined)).toBeTruthy();
    });
    it('fieldValidationIssues union', async () => {
        const stringOrNumberParam = (0, params_schema_1.RequiredField)(iots.union([iots.string, iots.number]));
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNumberParam, 1)).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNumberParam, 2)).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNumberParam, 'hello')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNumberParam, '')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNumberParam, true)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNumberParam, null)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNumberParam, undefined)).toBeTruthy();
    });
    it('fieldValidationIssues nullable', async () => {
        const stringOrNullParam = (0, params_schema_1.RequiredField)((0, params_schema_1.nullable)(iots.string));
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNullParam, 'hello')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNullParam, '')).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNullParam, null)).toBeUndefined();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNullParam, 1)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNullParam, true)).toBeTruthy();
        expect((0, params_schema_1.fieldValidationIssues)(stringOrNullParam, undefined)).toBeTruthy();
    });
});
const schema = {
    name: (0, params_schema_1.OptionalField)(iots.string),
    surname: (0, params_schema_1.RequiredField)(iots.string),
    lunch: (0, params_schema_1.RequiredField)(iots.boolean),
    age: (0, params_schema_1.OptionalField)(iots.number),
};
describe('validateParams', () => {
    it('validateParams', async () => {
        expect((0, params_schema_1.paramsValidationIssues)(schema, { surname: 'Doe', lunch: true }, { noExtra: true })).toBeUndefined();
        expect((0, params_schema_1.paramsValidationIssues)(schema, { name: 'John', surname: 'Doe', lunch: true }, { noExtra: true })).toBeUndefined();
        expect((0, params_schema_1.paramsValidationIssues)(schema, { surname: 'Doe', lunch: true, age: 29 }, { noExtra: true })).toBeUndefined();
        expect((0, params_schema_1.paramsValidationIssues)(schema, { name: 'John', surname: 'Doe', lunch: true, age: 29 }, { noExtra: true })).toBeUndefined();
        expect((0, params_schema_1.paramsValidationIssues)(schema, {}, { noExtra: true })).toBeTruthy();
        expect((0, params_schema_1.paramsValidationIssues)(schema, { name: 'John', surname: 'Doe', age: 29 }, { noExtra: true })).toBeTruthy(); // missing `lunch`
        expect((0, params_schema_1.paramsValidationIssues)(schema, { name: 'John', surname: 'Doe', lunch: true, age: 'old' }, { noExtra: true })).toBeTruthy(); // wrong type of `age`
        expect((0, params_schema_1.paramsValidationIssues)(schema, { surname: 'Doe', lunch: true, married: false }, { noExtra: true })).toBeTruthy(); // extra param `married`
        expect((0, params_schema_1.paramsValidationIssues)(schema, { surname: 'Doe', lunch: true, married: false })).toBeUndefined(); // extra param `married`
    });
});
describe('validateFullParams', () => {
    it('validateFullParams', async () => {
        expect((0, params_schema_1.paramsValidationIssues)(schema, { surname: 'Doe', lunch: true }, { requireAll: true, noExtra: true })).toBeTruthy();
        expect((0, params_schema_1.paramsValidationIssues)(schema, { name: 'John', surname: 'Doe', lunch: true }, { requireAll: true, noExtra: true })).toBeTruthy();
        expect((0, params_schema_1.paramsValidationIssues)(schema, { surname: 'Doe', lunch: true, age: 29 }, { requireAll: true, noExtra: true })).toBeTruthy();
        expect((0, params_schema_1.paramsValidationIssues)(schema, { name: 'John', surname: 'Doe', lunch: true, age: 29 }, { requireAll: true, noExtra: true })).toBeUndefined();
        expect((0, params_schema_1.paramsValidationIssues)(schema, {}, { requireAll: true, noExtra: true })).toBeTruthy();
        expect((0, params_schema_1.paramsValidationIssues)(schema, { name: 'John', surname: 'Doe', lunch: true, age: 'old' }, { requireAll: true, noExtra: true })).toBeTruthy(); // wrong type of `age`
        expect((0, params_schema_1.paramsValidationIssues)(schema, { name: 'John', surname: 'Doe', lunch: true, age: 29, married: true }, { requireAll: true, noExtra: true })).toBeTruthy(); // extra param `married`
        expect((0, params_schema_1.paramsValidationIssues)(schema, { name: 'John', surname: 'Doe', lunch: true, age: 29, married: true }, { requireAll: true, noExtra: false })).toBeUndefined(); // extra param `married`
    });
});
