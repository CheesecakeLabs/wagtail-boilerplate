const path = require('path')

module.exports = {
  alias: {
    _components: path.resolve(__dirname, '..', 'javascript/components'),
    _utils: path.resolve(__dirname, '..', 'javascript/utils'),
    _config: path.resolve(__dirname, '..', 'javascript/config'),
    _constants: path.resolve(__dirname, '..', 'javascript/constants'),
  },
}