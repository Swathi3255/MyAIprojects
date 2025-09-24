# Vercel Deployment Configuration

## Environment Variables

For production deployment on Vercel, you need to set the following environment variable in your Vercel dashboard:

- `VITE_API_URL`: Set this to your Vercel app URL (e.g., `https://your-app-name.vercel.app`)

## Local Development

For local development, the app will automatically use relative API paths (`/api/...`) when `VITE_API_URL` is not set.

## Deployment Steps

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set the environment variable `VITE_API_URL` in Vercel dashboard
4. Deploy!

The app will automatically build and deploy with the correct API configuration.
