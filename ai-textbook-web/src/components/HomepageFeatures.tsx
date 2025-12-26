import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';
import { BookOpen, Brain, Bot, Zap } from 'lucide-react';

type FeatureItem = {
  title: string;
  description: string;
  icon: React.ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'AI-Powered Learning',
    description: 'Leverage advanced AI to help you understand complex concepts in Physical AI and Humanoid Robotics through interactive conversations.',
    icon: <Brain className={styles.featureSvg} size={32} />,
  },
  {
    title: 'Interactive Textbook',
    description: 'Explore comprehensive content on Physical AI, robotics, and humanoid systems with an intelligent chatbot assistant.',
    icon: <BookOpen className={styles.featureSvg} size={32} />,
  },
  {
    title: 'Smart Assistant',
    description: 'Get instant answers to your questions about the textbook content with our RAG-powered AI assistant.',
    icon: <Bot className={styles.featureSvg} size={32} />,
  },
  {
    title: 'Real-time Help',
    description: 'Highlight text and ask questions about specific content sections for contextual understanding.',
    icon: <Zap className={styles.featureSvg} size={32} />,
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <div className={styles.contentCard}>
        <div className={styles.contentIconContainer}>
          {icon}
        </div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.contentSection}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2 className={styles.sectionTitle}>Core Features</h2>
            <p className={styles.sectionSubtitle}>Discover the powerful features that make learning Physical AI and Humanoid Robotics engaging and effective</p>
          </div>
        </div>
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}