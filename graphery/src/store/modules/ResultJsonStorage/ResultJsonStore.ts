import { RootState } from '@/store/states/state';

import {
  ResultJsonType,
  ResultJsonStateType,
  ResultJsonTypeFromQueryData,
  ResultJsonObjectType,
  KeysType,
  PositionType,
} from './ResultJsonStoreState';
import { ActionTree, GetterTree, MutationTree } from 'vuex';
import { newModelUUID } from '@/services/params';

const state: ResultJsonStateType = {
  resultJsonStringList: null,
  resultJsonObjectList: null,
  resultJsonPositions: {},
};

const mutations: MutationTree<ResultJsonStateType> = {
  LOAD_RESULT_JSON_STRING_LIST(state, value: ResultJsonType[]) {
    state.resultJsonStringList = value;
  },
  LOAD_RESULT_JSON_OBJECT_LIST(state, value: ResultJsonObjectType[]) {
    state.resultJsonObjectList = value;
  },
  LOAD_JSON_LOCATIONS(state, value: PositionType) {
    state.resultJsonPositions = value;
  },
  CHANGE_JSON_LOCATION(state, value: { positionId: string; position: number }) {
    state.resultJsonPositions[value.positionId].position = value.position;
  },
  CHANGE_RESULT_JSON_STRING(
    state,
    value: { json: string; graphId: string; codeId: string }
  ) {
    if (state.resultJsonStringList) {
      const result = state.resultJsonStringList.find(
        (obj) => obj.graphId === value.graphId && obj.codeId === value.codeId
      );
      if (result) {
        result.json = value.json;
      }
    }
  },
  CHANGE_RESULT_JSON_OBJECT(
    state,
    value: { jsonObject: object; graphId: string; codeId: string }
  ) {
    if (state.resultJsonObjectList) {
      const result = state.resultJsonObjectList.find(
        (obj) => obj.graphId === value.graphId && obj.codeId === value.codeId
      );
      if (result) {
        result.jsonObject = value.jsonObject;
      }
    }
  },

  // clear states
  CLEAR_RESULT_JSON_STRING_LIST(state) {
    state.resultJsonStringList = null;
  },
  CLEAR_RESULT_JSON_OBJECT_LIST(state) {
    state.resultJsonObjectList = null;
  },
  CLEAR_RESULT_JSON_STRING(state, value: KeysType) {
    if (state.resultJsonStringList) {
      const result = state.resultJsonStringList.find(
        (obj) => obj.graphId === value.graphId && obj.codeId === value.codeId
      );
      if (result) {
        result.json = '[]';
      }
    }
  },
  CLEAR_RESULT_JSON_STRING_BY_CODE_ID(state, codeId: string) {
    if (state.resultJsonStringList) {
      state.resultJsonStringList.forEach((obj) => {
        if (obj.codeId === codeId) {
          obj.json = '[]';
        }
      });
    }
  },
  CLEAR_RESULT_JSON_STRING_BY_GRAPH_ID(state, graphId: string) {
    if (state.resultJsonStringList) {
      state.resultJsonStringList.forEach((obj) => {
        if (obj.graphId === graphId) {
          obj.json = '[]';
        }
      });
    }
  },
  CLEAR_RESULT_JSON_OBJECT(state, value: KeysType) {
    if (state.resultJsonObjectList) {
      const result = state.resultJsonObjectList.find(
        (obj) => obj.graphId === value.graphId && obj.codeId === value.codeId
      );
      if (result) {
        result.jsonObject = [];
      }
    }
  },
  CLEAR_RESULT_JSON_OBJECT_BY_CODE_ID(state, codeId: string) {
    if (state.resultJsonObjectList) {
      state.resultJsonObjectList.forEach((obj) => {
        if (obj.codeId === codeId) {
          obj.jsonObject = [];
        }
      });
    }
  },
  CLEAR_RESULT_JSON_OBJECT_BY_GRAPH_ID(state, graphId: string) {
    if (state.resultJsonObjectList) {
      state.resultJsonObjectList.forEach((obj) => {
        if (obj.graphId === graphId) {
          obj.jsonObject = [];
        }
      });
    }
  },
};

function generateResultJsonObjectFromStringType(stringType: ResultJsonType) {
  return {
    jsonObject: stringType.json ? JSON.parse(stringType.json) : [],
    graphId: stringType.graphId,
    codeId: stringType.codeId,
  };
}

function generateResultJsonObjectList(stringList: ResultJsonType[]) {
  const objectList: ResultJsonObjectType[] = stringList.map(
    generateResultJsonObjectFromStringType
  );

  return objectList;
}

function findByKey(keys: KeysType) {
  return (obj: KeysType) =>
    obj.graphId === keys.graphId && obj.codeId === keys.codeId;
}

const actions: ActionTree<ResultJsonStateType, RootState> = {
  loadResultJsonListFromQueryData(
    { commit },
    resultJsonSet: ResultJsonTypeFromQueryData[]
  ) {
    const resultJsonStringList: ResultJsonType[] = resultJsonSet.map((obj) => {
      if (obj.json && obj.graph.id && obj.code.id) {
        return {
          json: obj.json,
          graphId: obj.graph.id,
          codeId: obj.code.id,
        };
      }
      return {
        json: '[]',
        graphId: newModelUUID,
        codeId: newModelUUID,
      };
    });
    const resultJsonObjectList = generateResultJsonObjectList(
      resultJsonStringList
    );

    commit('LOAD_RESULT_JSON_STRING_LIST', resultJsonStringList);
    commit('LOAD_RESULT_JSON_OBJECT_LIST', resultJsonObjectList);
  },
  loadResultJsonListFromMatched({ commit }, resultJsonSet: ResultJsonType[]) {
    const resultJsonObjectList = generateResultJsonObjectList(resultJsonSet);
    commit('LOAD_RESULT_JSON_STRING_LIST', resultJsonSet);
    commit('LOAD_RESULT_JSON_OBJECT_LIST', resultJsonObjectList);
  },
  changeResultJsonStringAndObject(
    { commit },
    resultJsonString: ResultJsonType
  ) {
    const objectType = generateResultJsonObjectFromStringType(resultJsonString);
    commit('CHANGE_RESULT_JSON_STRING', resultJsonString);
    commit('CHANGE_RESULT_JSON_OBJECT', objectType);
  },
  clearResultJsonStringByCodeId({ commit }, codeId: string) {
    commit('CLEAR_RESULT_JSON_STRING_BY_CODE_ID', codeId);
    commit('CLEAR_RESULT_JSON_OBJECT_BY_CODE_ID', codeId);
  },
  clearResultJsonStringAndObjectByIds({ commit }, keys: KeysType) {
    commit('CLEAR_RESULT_JSON_STRING', keys);
    commit('CLEAR_RESULT_JSON_OBJECT', keys);
  },
  CLEAR_ALL({ commit }) {
    commit('CLEAR_RESULT_JSON_STRING_LIST');
    commit('CLEAR_RESULT_JSON_OBJECT_LIST');
  },
};

const getters: GetterTree<ResultJsonStateType, RootState> = {
  resultJsonStringListEmpty(state) {
    return (
      state.resultJsonStringList && state.resultJsonStringList.length === 0
    );
  },
  resultJsonObjectListEmpty(state) {
    return (
      state.resultJsonObjectList && state.resultJsonObjectList.length === 0
    );
  },
  getCurrentJsonString: (state) => (keys: KeysType) => {
    return state.resultJsonStringList
      ? state.resultJsonStringList.find(findByKey(keys))
      : null;
  },
  getCurrentJsonObject: (state) => (keys: KeysType) => {
    return state.resultJsonObjectList
      ? state.resultJsonObjectList.find(findByKey(keys))
      : null;
  },
  getResultJsonObjectElement: (state, getter) => (
    keys: KeysType,
    position: number
  ) => {
    const jsonObject = getter.getCurrentJsonObject(keys);
    return jsonObject.jsonObject && jsonObject.jsonObject[position];
  },
  getResultJsonPositionObjectFromId: (state) => (positionId: string) => {
    return state.resultJsonPositions[positionId];
  },
  getResultJsonPositionFromId: (state) => (positionId: string) => {
    return state.resultJsonPositions[positionId].position;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
