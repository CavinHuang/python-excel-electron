import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import vitePluginImp from "vite-plugin-imp";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  build: {
    outDir: '../main/dist',
  },
  plugins: [
    react(),
    vitePluginImp({
      libList: [
        {
          libName: "antd",
          style: (name) => `antd/es/${name}/style`,
        },
      ],
    }),
  ],
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
        modifyVars: {
          "@primary-color": "#FF8140", //设置antd主题色
        },
      },
    },
  },
  resolve: {
    alias: [
      {
        find: "@",
        replacement: path.resolve(path.resolve(__dirname), "src"),
      },
      {
        find: "~antd",
        replacement: path.resolve(path.resolve(__dirname), "node_modules/antd"),
      },
    ],
  },
  server: {
    port: 3000,
  },
});
