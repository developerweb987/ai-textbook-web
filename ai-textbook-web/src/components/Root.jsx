import React from 'react';
import BookChatbot from './BookChatbot';

// Root component that wraps the entire Docusaurus application
const Root = ({ children }) => {
  return (
    <>
      {children}
      <BookChatbot />
    </>
  );
};

export default Root;