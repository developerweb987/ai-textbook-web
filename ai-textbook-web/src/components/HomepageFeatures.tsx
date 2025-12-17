import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';
import { BookOpen, Brain, Bot, Zap } from 'lucide-react';

type FeatureItem = {
  title: string;
  description: JSX.Element;
  icon: React.ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'AI-Powered Learning',
    icon: <Brain className="featureSvg" size={48} />,
    description: (
      <>
        Leverage advanced AI to help you understand complex concepts in Physical AI and Humanoid Robotics through interactive conversations.
      </>
    ),
  },
  {
    title: 'Interactive Textbook',
    icon: <BookOpen className="featureSvg" size={48} />,
    description: (
      <>
        Explore comprehensive content on Physical AI, robotics, and humanoid systems with an intelligent chatbot assistant.
      </>
    ),
  },
  {
    title: 'Smart Assistant',
    icon: <Bot className="featureSvg" size={48} />,
    description: (
      <>
        Get instant answers to your questions about the textbook content with our RAG-powered AI assistant.
      </>
    ),
  },
  {
    title: 'Real-time Help',
    icon: <Zap className="featureSvg" size={48} />,
    description: (
      <>
        Highlight text and ask questions about specific content sections for contextual understanding.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <div className="text--center">
        {icon}
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}