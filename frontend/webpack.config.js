const path = require("path");

module.exports = {
  entry: "./src/Index.tsx",
  mode: "production",
  output: {
    path: path.resolve(__dirname, "assets/js"),
    filename: "search.js",
    library: {
      name: "ChannelsDB",
      type: "var",
    },
  },
  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/,
        exclude: /node_modules/,
        use: "ts-loader",
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
};
