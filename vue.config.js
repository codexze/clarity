const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: "/",
  devServer: {
    proxy: {
      "^/api/": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        logLevel: "debug",
      },
      "^/ws/": {
        target: "ws://127.0.0.1:8000",
        ws: true,
        changeOrigin: true,
        logLevel: "debug",
      },
    },
    host: "localhost",
  },
});
