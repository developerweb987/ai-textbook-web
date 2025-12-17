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

## Complete Vercel Deployment Steps

### 1. Deploy Backend to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your GitHub repository (`ai-textbook-web`)
4. In the "Root Directory" dropdown, select `/backend`
5. Click "Next" and then "Deploy"
6. After deployment, note the backend URL (e.g., `https://your-backend-project-name.vercel.app`)

### 2. Configure Backend Environment Variables

1. Go to your deployed backend project in Vercel dashboard
2. Navigate to "Settings" → "Environment Variables"
3. Add the following variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `COHERE_API_KEY`: Your Cohere API key (if using)
   - `QDRANT_URL`: Qdrant Cloud URL (if using hosted service)
   - `QDRANT_API_KEY`: Qdrant API key (if using hosted service)
   - `DATABASE_URL`: Database connection string (for production DB)
   - `CORS_ORIGINS`: Comma-separated list of allowed origins (the default includes Vercel URLs)

### 3. Deploy Frontend to Vercel

1. Go back to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import the same GitHub repository (`ai-textbook-web`)
4. In the "Root Directory" dropdown, select `/ai-textbook-web`
5. Add the following environment variable:
   - `REACT_APP_BACKEND_URL`: Set to your deployed backend URL from step 1
6. Click "Deploy"

### 4. Configure Frontend Environment Variables

1. Go to your deployed frontend project in Vercel dashboard
2. Navigate to "Settings" → "Environment Variables"
3. Add the following variable:
   - `REACT_APP_BACKEND_URL`: Your deployed backend URL (e.g., `https://your-backend-project-name.vercel.app`)

### 5. Verify the Deployment

1. Access your frontend URL (e.g., `https://your-frontend-project-name.vercel.app`)
2. Open the chatbot and test functionality
3. Verify that:
   - The chat window opens and closes properly
   - Selected text functionality works
   - Messages are sent and received without CORS errors
   - The chat maintains session state
   - API responses are properly formatted

### 6. Optional: Custom Domain Setup

1. In your Vercel dashboard, go to your frontend project
2. Navigate to "Settings" → "Domains"
3. Add your custom domain
4. Follow Vercel's instructions to update your DNS settings
5. Update your CORS settings in the backend to include your custom domain

## Production Considerations

### Database Configuration
- For production, consider using PostgreSQL instead of SQLite
- Set up a managed database service (e.g., Vercel Postgres, AWS RDS)
- Update `DATABASE_URL` environment variable accordingly

### Vector Database (Qdrant)
- For production, use Qdrant Cloud or self-hosted Qdrant instance
- Configure `QDRANT_URL` and `QDRANT_API_KEY` environment variables
- Ensure your Qdrant instance is properly secured and scaled

### AI API Keys Security
- Never hardcode API keys in your source code
- Always use environment variables for API keys
- Consider using Vercel's secret management for sensitive keys

### Performance Optimization
- Monitor your serverless function cold starts
- Consider using Vercel's edge functions for better performance
- Optimize your AI model calls and caching strategies