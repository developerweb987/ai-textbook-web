import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import BookContentSection from '@site/src/components/BookContentSection';
import BookChatbot from '@site/src/components/BookChatbot';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className={styles.heroContainer}>
        <div className={styles.heroContent}>
          {/* Left side: Text content */}
          <div className={styles.heroText}>
            <h1 className={styles.heroTitle}>{siteConfig.title}</h1>
            <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
            <div className={styles.buttons}>
              <Link
                className={clsx('button button--primary button--lg', styles.primaryButton)}
                to="/docs/introduction/intro">
                Start Learning
              </Link>
              <Link
                className={clsx('button button--secondary button--outline button--lg', styles.secondaryButton)}
                to="/docs/introduction">
                Explore Modules
              </Link>
            </div>
          </div>

          {/* Right side: Hero image */}
          <div className={styles.heroIllustration}>
            <img
              src="/img/img_hero.png"
              alt="AI Textbook Hero"
              className={styles['hero-image']}
            />
          </div>
        </div>

        {/* Background particles */}
        <div className={styles.particles}>
          <div className={clsx(styles.particle, styles['particle-1'])}></div>
          <div className={clsx(styles.particle, styles['particle-2'])}></div>
          <div className={clsx(styles.particle, styles['particle-3'])}></div>
          <div className={clsx(styles.particle, styles['particle-4'])}></div>
          <div className={clsx(styles.particle, styles['particle-5'])}></div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): React.JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <BookContentSection />
      </main>
      <BookChatbot />
    </Layout>
  );
}