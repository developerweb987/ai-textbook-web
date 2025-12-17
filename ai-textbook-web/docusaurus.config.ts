import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'An AI-Native Textbook on Physical AI and Humanoid Robotics',
  favicon: 'img/ai-favicon.svg',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  trailingSlash: undefined, // Let Docusaurus handle trailing slashes appropriately

  // Set the production url of your site here
  url: 'https://ai-textbook-web.vercel.app',  // Updated for Vercel deployment
  // Set the /<baseUrl>/ pathname under which your site is served
  // For Vercel deployment, keep as '/' unless using a subdirectory
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'developerweb987', // Usually your GitHub org/user name.
  projectName: 'physical-ai-textbook', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/developerweb987/physical-ai-textbook/tree/main/ai-textbook-web/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
    [
      '@docusaurus/plugin-sitemap',
      {
        changefreq: 'weekly',
        priority: 0.5,
        ignorePatterns: ['/tags/**'],
        filename: 'sitemap.xml',
      },
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI Textbook',
      logo: {
        alt: 'Physical AI & Humanoid Robotics Textbook',
        src: 'img/ai-textbook-logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'textbookSidebar',
          position: 'left',
          label: 'Book Docs',
        },
        {
          href: 'https://github.com/developerweb987/physical-ai-textbook.git',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Textbook Modules',
          items: [
            {
              label: 'Introduction to Physical AI',
              to: '/docs/introduction',
            },
            {
              label: 'Theory & Fundamentals',
              to: '/docs/theory-fundamentals',
            },
            {
              label: 'Locomotion & Manipulation',
              to: '/docs/locomotion-manipulation',
            },
            {
              label: 'Perception & Control',
              to: '/docs/perception-control',
            },
          ],
        },
        {
          title: 'Advanced Topics',
          items: [
            {
              label: 'Advanced Control Systems',
              to: '/docs/applications-implementation/advanced-control-strategies',
            },
            {
              label: 'Human-Robot Interaction',
              to: '/docs/advanced-topics/human-robot-interaction',
            },
            {
              label: 'Multi-Robot Systems',
              to: '/docs/advanced-topics/multi-robot-systems',
            },
            {
              label: 'Embodied Intelligence',
              to: '/docs/advanced-topics/embodied-ai-cognition',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'GitHub Repository',
              href: 'https://github.com/developerweb987/physical-ai-textbook.git',
            },
            {
              label: 'Research Papers',
              href: 'https://scholar.google.com/scholar?q=physical+ai+humanoid+robotics',
            },
            {
              label: 'AI & Robotics Community',
              href: 'https://discordapp.com/invite/physical-ai',
            },
            {
              label: 'Contributing Guide',
              to: '/docs/references',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Empowering the next generation of roboticists and AI researchers.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'docker', 'json'],
    },
    metadata: [
      {name: 'keywords', content: 'robotics, physical AI, humanoid robots, AI, machine learning, control systems'},
      {name: 'description', content: 'Comprehensive textbook on Physical AI and Humanoid Robotics'},
      {property: 'og:title', content: 'Physical AI & Humanoid Robotics Textbook'},
      {property: 'og:description', content: 'Master Physical AI, robotics, and humanoid systems with this comprehensive textbook'},
      {property: 'og:type', content: 'website'},
      {property: 'og:url', content: 'https://ai-textbook-web.vercel.app/'},
    ],
  } satisfies Preset.ThemeConfig,

  // Add the Root component to wrap the entire application
  clientModules: [
    require.resolve('./src/components/Root.jsx'),
  ],
};

export default config;
