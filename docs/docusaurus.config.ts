import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

const config: Config = {
  title: "Ldx-Insight",
  tagline: "Hệ thống chia sẻ thông tin nguồn mở Ldx-Insight",
  favicon: "img/favicon.ico",

  url: "https://Haui-HIT-NhoNguoiYeuCu.github.io",
  baseUrl: "/Ldx-Insight/",

  organizationName: "Haui-HIT-NhoNguoiYeuCu",
  projectName: "Ldx-Insight",

  onBrokenLinks: "throw",

  i18n: {
    defaultLocale: "vi",
    locales: ["vi"],
  },

  /** ✅ Bật Mermaid trong Markdown */
  markdown: { mermaid: true },

  /** ✅ Thêm theme Mermaid */
  themes: ["@docusaurus/theme-mermaid"],

  /** ✅ KaTeX CSS để render công thức toán */
  stylesheets: [
    {
      href: "https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css",
      type: "text/css",
      // integrity/crossorigin có thể bổ sung nếu bạn muốn, nhưng để tránh lệch version thì có thể bỏ trống.
    },
  ],

  presets: [
    [
      "classic",
      {
        docs: false,
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      "@docusaurus/plugin-content-docs",
      {
        id: "overview",
        path: "overview-docs",
        routeBasePath: "overview",
        sidebarPath: "./sidebarsOverview.ts",
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
      },
    ],
    [
      "@docusaurus/plugin-content-docs",
      {
        id: "backend",
        path: "backend-docs",
        routeBasePath: "backend",
        sidebarPath: "./sidebarsBackend.ts",
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
      },
    ],
    [
      "@docusaurus/plugin-content-docs",
      {
        id: "frontend",
        path: "frontend-docs",
        routeBasePath: "frontend",
        sidebarPath: "./sidebarsFrontend.ts",
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
      },
    ],
    [
      "@docusaurus/plugin-content-docs",
      {
        id: "ml-ai",
        path: "ml-ai-docs",
        routeBasePath: "ml-ai",
        sidebarPath: "./sidebarsMlAi.ts",
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
      },
    ],
    [
      "@docusaurus/plugin-content-docs",
      {
        id: "infrastructure",
        path: "infrastructure-docs",
        routeBasePath: "infrastructure",
        sidebarPath: "./sidebarsInfrastructure.ts",
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
      },
    ],
    // Nếu bạn có "presentation" như cấu hình trước đó, bật lại block dưới đây:
    // [
    //   "@docusaurus/plugin-content-docs",
    //   {
    //     id: "presentation",
    //     path: "bai-thuyet-trinh",
    //     routeBasePath: "presentation",
    //     sidebarPath: "./sidebarsPresentation.ts",
    //     remarkPlugins: [remarkMath],
    //     rehypePlugins: [rehypeKatex],
    //   },
    // ],
  ],

  themeConfig: {
    image: "img/social-card.jpg",
    colorMode: { respectPrefersColorScheme: true },
    navbar: {
      title: "Ldx-Insight",
      logo: { alt: "Ldx-Insight Logo", src: "img/logo.svg" },
      items: [
        {
          to: "/overview/intro",
          label: "System Overview",
          position: "left",
          activeBaseRegex: `/overview/`,
        },
        {
          to: "/backend/overview",
          label: "Backend",
          position: "left",
          activeBaseRegex: `/backend/`,
        },
        {
          to: "/frontend/overview",
          label: "Frontend",
          position: "left",
          activeBaseRegex: `/frontend/`,
        },
        {
          to: "/ml-ai/intro",
          label: "ML/AI",
          position: "left",
          activeBaseRegex: `/ml-ai/`,
        },
        {
          to: "/infrastructure/intro",
          label: "Infrastructure",
          position: "left",
          activeBaseRegex: `/infrastructure/`,
        },
        {
          href: "https://github.com/Haui-HIT-NhoNguoiYeuCu/Ldx-Insight.git",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
