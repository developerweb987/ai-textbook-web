# Vercel Deployment Guide

This guide explains how to deploy the full-stack Physical AI textbook application to Vercel.

## Prerequisites

- A Vercel account (sign up at https://vercel.com)
- The GitHub repository connected to your Vercel account

## Deployment Steps

### 1. Deploy the Backend

1. Go to https://vercel.com/dashboard
2. Click "New Project" and connect to your GitHub repository
3. Import the `ai-textbook-web` repository
4. When prompted for the project configuration:
   - Framework: None (or "Other framework")
   - Root Directory: `/backend`
5. Set the following environment variables in the Vercel dashboard:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here (optional)
   QDRANT_API_KEY=your_qdrant_api_key_here (optional)
   DATABASE_URL=sqlite+aiosqlite:///./physical_ai_textbook.db
   CORS_ORIGINS=https://your-frontend-url.vercel.app,http://localhost:3000,http://localhost:8000
   ```
6. Click "Deploy" to deploy the backend

### 2. Deploy the Frontend

1. Go to https://vercel.com/dashboard
2. Click "New Project" and connect to your GitHub repository again
3. Import the same `ai-textbook-web` repository
4. When prompted for the project configuration:
   - Framework: Detect automatically (should detect Docusaurus)
   - Root Directory: `/ai-textbook-web`
5. Set the following environment variables:
   ```
   REACT_APP_BACKEND_URL=https://your-backend-project-name.vercel.app
   ```
6. Click "Deploy" to deploy the frontend

## Post-Deployment Configuration

### Update CORS Settings

After deploying both frontend and backend, you'll need to update the CORS settings in your backend environment variables to include your frontend's Vercel URL:

```
CORS_ORIGINS=https://your-frontend-project-name.vercel.app,https://your-frontend-project-name-git-main.your-account.vercel.app,http://localhost:3000
```

### Database Configuration for Production

⚠️ **Important Serverless Considerations**:

- Serverless functions have ephemeral filesystems - SQLite database files may not persist between requests
- For production deployments, consider using PostgreSQL or another cloud database
- Update DATABASE_URL to use a cloud database service for production

### Vector Database (Qdrant)

- Qdrant should be deployed as a separate service
- Use the hosted Qdrant Cloud or self-hosted Qdrant instance
- Update QDRANT_URL and QDRANT_API_KEY accordingly

### Environment Variables Reference

#### Backend Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Qdrant vector database URL (if using hosted service)
- `QDRANT_API_KEY`: Qdrant API key (if using hosted service)
- `DATABASE_URL`: Database connection string
- `CORS_ORIGINS`: Comma-separated list of allowed origins (already includes Vercel URLs)

#### Frontend Environment Variables
- `REACT_APP_BACKEND_URL`: URL of your deployed backend

## Testing the Deployment

1. Access your frontend at the URL provided by Vercel (e.g., `https://your-frontend-project-name.vercel.app`)
2. Test the chatbot functionality
3. Verify that API calls to the backend are working without CORS errors
4. Test text selection and conversation features

## Troubleshooting

### CORS Issues
- Ensure `CORS_ORIGINS` includes your frontend's domain
- Check that the backend environment variables are properly set

### API Connection Issues
- Verify that `REACT_APP_BACKEND_URL` points to your deployed backend
- Check that the backend is properly deployed and accessible

### Build Failures
- Ensure all dependencies are properly listed in package.json and requirements.txt
- Check that the build commands match your project setup