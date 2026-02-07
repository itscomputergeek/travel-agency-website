# Deploy Travel Agency Website to Render

Your Django project is now configured for Render deployment! Follow these steps:

## Files Created for Deployment ✅

- ✅ `requirements.txt` - Updated with production packages
- ✅ `build.sh` - Build script for Render
- ✅ `render.yaml` - Render configuration
- ✅ `.env.example` - Environment variables template
- ✅ Updated `settings.py` - Production-ready configuration

## Step-by-Step Deployment Guide

### 1. Commit and Push Changes to GitHub

```bash
git add .
git commit -m "Configure for Render deployment"
git push origin master
```

### 2. Sign Up / Login to Render

1. Go to https://render.com
2. Sign up or login (use GitHub to sign in for easier integration)
3. Connect your GitHub account

### 3. Create a New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `itscomputergeek/travel-agency-website`
3. Grant Render permission to access the repository

### 4. Configure Your Web Service

**Basic Settings:**
- **Name:** `travel-agency-website` (or any name you prefer)
- **Region:** Choose closest to you
- **Branch:** `master`
- **Runtime:** `Python 3`
- **Build Command:** `bash build.sh`
- **Start Command:** `gunicorn travel_agency.wsgi:application`

**Instance Type:**
- Select **"Free"** tier (perfect for getting started)

### 5. Set Environment Variables

Click on **"Environment"** tab and add these variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.8` |
| `DEBUG` | `False` |
| `SECRET_KEY` | Click "Generate" to create a random secret key |
| `ALLOWED_HOSTS` | `.onrender.com` |

### 6. Create PostgreSQL Database

1. Go to **Dashboard** → **"New +"** → **"PostgreSQL"**
2. **Name:** `travel-agency-db`
3. **Database:** `travel_agency_db`
4. **User:** `travel_agency_user`
5. **Region:** Same as your web service
6. **Instance Type:** **"Free"** tier
7. Click **"Create Database"**

### 7. Link Database to Web Service

1. Go back to your **Web Service** settings
2. In **Environment** tab, add:
   - **Key:** `DATABASE_URL`
   - **Value:** Click "From Database" → Select your PostgreSQL database → Copy "Internal Database URL"

### 8. Deploy!

1. Click **"Create Web Service"**
2. Render will automatically:
   - Install dependencies from `requirements.txt`
   - Run `collectstatic` to gather static files
   - Run `migrate` to set up database
   - Start your Django app with Gunicorn

### 9. Monitor Deployment

- Watch the **Logs** tab to see deployment progress
- First deployment takes 5-10 minutes
- Look for: "Your service is live" message

### 10. Access Your Website!

Once deployed, your website will be available at:
```
https://travel-agency-website.onrender.com
```
(Replace with your actual service name)

## Post-Deployment Tasks

### Create Admin User

After first deployment:

1. Go to **Shell** tab in Render dashboard
2. Run:
```bash
python manage.py createsuperuser
```
3. Follow prompts to create admin account

### Import Travel Packages

In the Shell tab:
```bash
python manage.py import_packages
```

### Access Admin Panel

Visit: `https://your-app.onrender.com/admin/`

## Important Notes

⚠️ **Free Tier Limitations:**
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free (enough for one service)
- Database limited to 1GB storage

✅ **Static Files:**
- WhiteNoise serves static files (CSS, JS, images)
- No need for separate CDN on free tier

✅ **Media Files:**
- User uploads work locally
- For production, consider Cloudinary or AWS S3

## Troubleshooting

### Build Fails?
- Check **Logs** tab for errors
- Common issues:
  - Missing dependencies in `requirements.txt`
  - Wrong Python version
  - Database connection issues

### Database Errors?
- Ensure `DATABASE_URL` environment variable is set correctly
- Check database is in same region as web service

### Static Files Not Loading?
- Run `python manage.py collectstatic` in Shell
- Check `STATIC_ROOT` and `STATICFILES_STORAGE` in settings.py

### App Not Responding?
- Free tier spins down - first request wakes it up
- Check logs for errors

## Updating Your App

Every time you push to GitHub:
```bash
git add .
git commit -m "Your update message"
git push origin master
```

Render automatically:
- Detects the push
- Rebuilds your app
- Deploys new version

## Need Help?

- Render Docs: https://render.com/docs/deploy-django
- Render Community: https://community.render.com/

---

**Your travel agency website is ready for the world!** 🚀🌍
