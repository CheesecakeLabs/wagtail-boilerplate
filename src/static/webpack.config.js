const path = require('path')

const webpack = require('webpack')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const BundleTracker = require('webpack-bundle-tracker')

const resolve = require('./webpack/resolve')

module.exports = {
  entry: path.resolve(__dirname, './javascript/app.js'),
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new BundleTracker({ filename: '../../bundles/webpack-stats.json' }),
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css',
    }),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.css$/,
        exclude: /node_modules/,
        use: [{ loader: MiniCssExtractPlugin.loader }, 'css-loader', 'postcss-loader'],
      },
      {
        test: /\.(eot|svg|ttf|woff|woff2|otf)$/,
        exclude: [/node_modules/, /icons/],
        use: 'file-loader?name=./fonts/[name].[ext]',
      },
      {
        test: /\.css$/,
        include: /node_modules/,
        use: [{ loader: MiniCssExtractPlugin.loader }, 'css-loader'],
      },
      {
        test: /\.(jpe?g|png|svg)$/i,
        use: ['file-loader?hash=sha512&digest=hex&name=img/[hash].[ext]', 'image-webpack-loader?'],
      },
      {
        test: /\.html$/,
        use: 'raw-loader',
      },
    ],
  },
  output: {
    path: path.resolve(__dirname, '../../bundles'),
    filename: '[name].js',
  },
  resolve,
}
