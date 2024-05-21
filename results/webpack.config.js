const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');

module.exports = {
  entry: {
    ChannelsDB: './ChannelsDB/src/App.tsx',
  },
  output: {
    filename: '[name]-Core.js?version=R1.1.9.1',
    path: path.resolve(__dirname, 'dist/ChannelsDB'),
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [
        { from: './ChannelsDB/js/scripts.js', to: () => { return `js/[name][ext]`;} },
        { from: './ChannelsDB/css/styles.css', to: () => { return `css/[name][ext]`;} },
        { from: './ChannelsDB/fonts/*', to: () => { return `fonts/[name][ext]`;} },
        { from: './ChannelsDB/images/*', to: () => { return `images/[name][ext]`;} },
        { from: './ChannelsDB/index.html', to: 'index.html' },
      ]
    }),
  ],
  resolve: {
    extensions: ['.tsx', '.ts', '.js', '.scss', '.css'],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader'],
        sideEffects: true,
      },
    ],
  },
};