import React from 'react';
import clsx from 'clsx';
import styles from './BookContentSection.module.css';
import { BookOpen, GraduationCap, Library, Lightbulb } from 'lucide-react';

type ContentItem = {
  title: string;
  description: string;
  icon: React.ReactNode;
};

const ContentList: ContentItem[] = [
  {
    title: 'Comprehensive Learning',
    description: 'Master Physical AI and Humanoid Robotics through structured modules that build from fundamentals to advanced concepts.',
    icon: <GraduationCap className={styles.featureSvg} size={32} />,
  },
  {
    title: 'Interactive Textbook',
    description: 'Engage with interactive content that brings complex robotics concepts to life through visualizations and examples.',
    icon: <BookOpen className={styles.featureSvg} size={32} />,
  },
  {
    title: 'Knowledge Library',
    description: 'Access a curated collection of resources, research papers, and references to deepen your understanding.',
    icon: <Library className={styles.featureSvg} size={32} />,
  },
  {
    title: 'AI-Powered Insights',
    description: 'Get intelligent explanations and insights that help you understand complex theoretical and practical concepts.',
    icon: <Lightbulb className={styles.featureSvg} size={32} />,
  },
];

function ContentCard({ title, description, icon }: ContentItem) {
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

export default function BookContentSection(): JSX.Element {
  return (
    <section className={styles.contentSection}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2 className={styles.sectionTitle}>Enhance Your Learning Journey</h2>
            <p className={styles.sectionSubtitle}>Discover the comprehensive resources designed to advance your understanding of Physical AI and Humanoid Robotics</p>
          </div>
        </div>
        <div className="row">
          {ContentList.map((props, idx) => (
            <ContentCard key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}