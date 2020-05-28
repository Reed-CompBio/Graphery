module.exports = {
  preset: '@vue/cli-plugin-unit-jest/presets/typescript-and-babel',
  collectCoverage: true,
  collectCoverageFrom: ['**/*.{js,jsx,ts,vue}', '!**/node_modules/**'],
};
