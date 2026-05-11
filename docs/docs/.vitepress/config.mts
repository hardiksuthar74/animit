import { defineConfig } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";

// https://vitepress.dev/reference/site-config
const viteConfig = defineConfig({
  title: "Animit",
  description: "An anime tracker app",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Examples", link: "/markdown-examples" },
    ],

    sidebar: [
      {
        text: "Getting Started",
        items: [{ text: "Overview", link: "/overview" }],
      },
      {
        text: "Core Modules",
        items: [
          { text: "Authentication", link: "/authentication" },
          { text: "Onboard", link: "/onboard" },
          { text: "Anime", link: "/anime" },
          { text: "User Anime", link: "/user-anime" },
          { text: "Discovery", link: "/discovery" },
          { text: "Recommendation", link: "/recommendation" },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/vuejs/vitepress" },
    ],
  },
});

export default withMermaid(viteConfig);
