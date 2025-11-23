import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { configDefaults } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  },
  test: {
    globals: true,          // ← enables test(), expect(), vi()
    environment: "jsdom",   // ← required for React DOM tests
    setupFiles: "./src/tests/setup.ts",
  },
});
