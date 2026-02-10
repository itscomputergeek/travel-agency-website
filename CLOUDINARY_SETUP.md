# Cloudinary Setup Guide

Cloudinary is required for storing media files (package images) on Render, as Render's filesystem is ephemeral and doesn't persist uploaded files between deployments.

## Step 1: Create Free Cloudinary Account

1. Go to https://cloudinary.com/users/register_free
2. Sign up for a **free account** (no credit card required)
3. Verify your email address

## Step 2: Get Your Credentials

1. Log in to your Cloudinary dashboard: https://cloudinary.com/console
2. On the dashboard, you'll see your credentials:
   - **Cloud Name**: (e.g., `dxxxxxxxxxxx`)
   - **API Key**: (e.g., `123456789012345`)
   - **API Secret**: (click "👁 Show" to reveal)

## Step 3: Add Credentials to Render

1. Go to your Render dashboard: https://dashboard.render.com/
2. Find your **travel-agency-website** service
3. Click on it, then go to **"Environment"** tab
4. Add these environment variables:

   ```
   CLOUDINARY_CLOUD_NAME=your-cloud-name-here
   CLOUDINARY_API_KEY=your-api-key-here
   CLOUDINARY_API_SECRET=your-api-secret-here
   ```

5. Click **"Save Changes"**

## Step 4: Redeploy

After saving the environment variables, Render will automatically trigger a new deployment. This deployment will:

1. Install Cloudinary packages
2. Configure Django to use Cloudinary for media files
3. Download all 46 packages × 5 images = 230 images
4. Upload them automatically to Cloudinary
5. Images will now persist and display correctly!

## Verification

Once deployment completes (~5-8 minutes):

1. Visit: https://travel-agency-website-w66b.onrender.com/
2. All package images should now display correctly
3. Images are stored on Cloudinary's CDN (fast and reliable)

## Cloudinary Free Tier

The free tier includes:
- ✅ 25 GB storage
- ✅ 25 GB bandwidth/month
- ✅ 25,000 transformations/month
- ✅ More than enough for this project!

## Need Help?

If you have any issues, check:
1. Credentials are correct (no extra spaces)
2. All 3 environment variables are set on Render
3. Deployment completed successfully
4. Check Render logs for any errors
