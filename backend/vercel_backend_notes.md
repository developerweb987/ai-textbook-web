# Vercel Backend Deployment Notes

## Important Considerations for Serverless Deployment

### Database Limitations
- Serverless functions have ephemeral filesystems
- SQLite database files may not persist between requests
- For production deployments, consider using PostgreSQL or another cloud database
- Update DATABASE_URL to use a cloud database service for production

### Vector Database (Qdrant)
- Qdrant should be deployed as a separate service
- Use the hosted Qdrant Cloud or self-hosted Qdrant instance
- Update QDRANT_URL and QDRANT_API_KEY accordingly

### Startup Time
- First requests may be slow due to cold starts
- AI model initialization happens on first request
- Consider implementing a warm-up endpoint if needed

### File Size Limitations
- Vercel serverless functions have a 50MB limit
- Large dependencies may cause deployment failures
- Optimize requirements.txt for production

### Environment Configuration
```env
# For Vercel deployment
DATABASE_URL=postgresql://username:password@host:port/database_name
QDRANT_URL=https://your-cluster-url.qdrant.tech:6333
QDRANT_API_KEY=your_api_key
GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
CORS_ORIGINS=https://your-frontend.vercel.app,https://yourdomain.com
```

### Alternative: Vercel with Redis/PostgreSQL Add-ons
Consider using Vercel's database add-ons for a more robust deployment:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "env": {
    "DATABASE_URL": "@your-postgres-database"
  }
}
```