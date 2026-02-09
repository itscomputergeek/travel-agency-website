# Pexels API Setup Guide

This guide will help you get a **free API key** from Pexels to automatically fetch beautiful travel images for all 49 packages.

## Why Pexels?
- ✅ **100% Free** - No credit card required
- ✅ **High Quality** - Professional travel photography
- ✅ **No Attribution Required** - Free to use commercially
- ✅ **200 requests/hour** - Enough for all packages
- ✅ **20,000 requests/month** - Very generous free tier

## Step-by-Step Instructions

### 1. Sign Up for Pexels API

1. Go to **https://www.pexels.com/api/**
2. Click on **"Get Started"** or **"Sign Up"**
3. Create a free account with your email
4. Verify your email address

### 2. Create an API Application

1. Once logged in, click on **"Your Applications"** or go to **https://www.pexels.com/api/new/**
2. Fill in the application form:
   - **App Name**: `Travel Agency Website` (or any name you prefer)
   - **App Description**: `Fetching travel destination images for tour packages`
   - **App URL**: `https://travel-agency-website-w66b.onrender.com` (your Render URL)
3. Click **"Generate API Key"**

### 3. Copy Your API Key

1. You'll see your API key displayed (looks like: `abcd1234efgh5678ijkl9012mnop3456`)
2. **IMPORTANT**: Copy this key - you'll need it in the next step

### 4. Add API Key to Render

1. Go to your Render dashboard: **https://dashboard.render.com/**
2. Click on your **travel-agency-website** service
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `PEXELS_API_KEY`
   - **Value**: Paste your API key from step 3
6. Click **"Save Changes"**

### 5. Deploy to Render

1. In Render dashboard, click **"Manual Deploy"** → **"Deploy latest commit"**
2. OR simply push any changes to GitHub, and Render will auto-deploy
3. The build script will automatically:
   - Import all 49 packages from Word documents
   - Fetch 5 beautiful images for each package from Pexels
   - Save them to your database

### 6. Verify Images Were Fetched

After deployment completes (5-10 minutes):

1. Visit your admin panel: **https://travel-agency-website-w66b.onrender.com/admin**
2. Login with:
   - Username: `admin`
   - Password: `TravelAdmin2026`
3. Click on **"Packages"**
4. Open any package and scroll down to see the 5 images:
   - Featured Image
   - Image 2
   - Image 3
   - Image 4
   - Image 5

## Local Development (Optional)

To test image fetching locally:

1. Create a `.env` file in your project root (copy from `.env.example`)
2. Add your API key to `.env`:
   ```
   PEXELS_API_KEY=your-api-key-here
   ```
3. Run the command manually:
   ```bash
   python manage.py fetch_package_images
   ```

## Troubleshooting

### No images were fetched
- Check that `PEXELS_API_KEY` is set correctly in Render environment variables
- Check the build logs for any error messages
- Verify your API key is valid at https://www.pexels.com/api/

### API rate limit exceeded
- Free tier: 200 requests/hour, 20,000/month
- With 49 packages × 5 images = 245 requests total
- If you hit the limit, wait 1 hour and redeploy

### Images are not showing on package pages
- Clear your browser cache
- Check that the images were saved in the admin panel
- Verify MEDIA_URL and MEDIA_ROOT settings are correct

## Need Help?

If you encounter any issues:
1. Check the deployment logs in Render dashboard
2. Look for error messages related to `fetch_package_images`
3. Verify all environment variables are set correctly

---

**That's it!** Your travel agency website will now have beautiful, professional images for all 49 packages automatically! 🎉
