'use strict';

function subscript(state, silent) {
  let found, token;
  const max = state.posMax,
    start = state.pos;

  // if it does not start with ~ then stop
  if (state.src.charCodeAt(start) !== 0x40 /* @ */) {
    return false;
  }

  // if it's silent, stop
  if (silent) {
    return false;
  } // don't run any pairs in validation mode

  // if the length is smaller than or equal to 2, stop
  if (start + 2 >= max) {
    return false;
  }

  // next position
  state.pos = start + 1;

  // find next ~
  while (state.pos < max) {
    if (state.src.charCodeAt(state.pos) === 0x40 /* @ */) {
      found = true;
      break;
    }

    state.md.inline.skipToken(state);
  }

  // if not found or the end stop
  if (!found || start + 1 === state.pos) {
    // move the pos to the original start
    state.pos = start;
    return false;
  }

  // get the content between two ~ ~
  const content = Number(state.src.slice(start + 1, state.pos));

  // don't allow unescaped spaces/newlines inside
  if (!Number.isInteger(content) || content <= 0) {
    state.pos = start;
    return false;
  }

  // found!
  state.posMax = state.pos;
  state.pos = start + 1;

  // Earlier we checked !silent, but this implementation does not need it
  token = state.push('bp_open', 'span', 1);
  token.attrJoin('class', 'tutorial-breakpoint');
  token.attrJoin('position', content);
  token.markup = '@';

  token = state.push('text', '', 0);
  token.content = content;

  token = state.push('bp_close', 'span', -1);
  token.markup = '@';

  state.pos = state.posMax + 1;
  state.posMax = max;
  return true;
}

module.exports = function breakpointPlugin(md) {
  md.inline.ruler.after('emphasis', 'bp', subscript);
};
