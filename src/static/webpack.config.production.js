const webpack = require("webpack")
const path = require("path")
const ExtractTextPlugin = require("extract-text-webpack-plugin")
const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  entry: {
    main: "./javascript/app",
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        screw_ie8: true,
        warnings: false,
      },
    }),
    new ExtractTextPlugin("main.css"),
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("production"),
    }),
    new BundleTracker({filename: '../.dist/webpack-stats.json'}),
  ],
  module: {
    loaders: [
      {
        test: /\.js$/,
        loader: "babel-loader",
        exclude: /node_modules/,
        query: {
          presets: ["es2015"],
        },
      },
      {
        test: /\.css$/,
        exclude: /node_modules/,
        use: ExtractTextPlugin.extract({
          use: [
            {
              loader: "css-loader",
              options: {
                minimize: true,
                importLoaders: 1,
                config: {
                  path: "./postcss.config.js",
                },
              },
            },
            "postcss-loader",
          ],
        }),
      },
      {
        test: /\.css$/,
        include: /node_modules/,
        loader: ExtractTextPlugin.extract({
          fallback: "style-loader",
          use: [
            {
              loader: "css-loader",
              options: {
                modules: false,
                minimize: true,
              },
            },
          ],
        }),
      },
      {
        test: /\.(jpe?g|png|svg)$/i,
        loaders: ["file-loader?hash=sha512&digest=hex&name=[hash].[ext]", "image-webpack-loader?"],
      },
    ],
  },
  output: {
    path: path.resolve(__dirname, "../.dist/"),
    filename: "main.js",
  },
}
