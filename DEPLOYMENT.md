# 🚀 Deployment Guide - YogaFlow AI

Complete guide to deploy YogaFlow AI for **FREE** using **Vercel** (Frontend) and **Render** (Backend).

---

## 📋 What You Need

- [x] GitHub account (you already have this)
- [ ] Vercel account → https://vercel.com (sign up with GitHub)
- [ ] Render account → https://render.com (sign up with GitHub)

**Total time: ~15-20 minutes**

---

## 🎯 Architecture

```
Frontend (Next.js) → Vercel (free unlimited)
Backend (FastAPI)  → Render (free 750 hours/month)
```

---

## 🔧 STEP 1: Push Code to GitHub

Make sure all code is pushed:

```bash
git add .
git commit -m "Resolve merge conflicts and add deployment config"
git push origin main
```

---

## 🖥️ STEP 2: Deploy Backend to Render

### 2.1 Create Account & Login

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with **GitHub**
4. Authorize Render to access your repositories

### 2.2 Deploy Backend

1. In Render dashboard, click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Search and select: `ve11yn/yoga-pose-correction`
   - Click **"Connect"**

3. **Configure Service:**
   ```
   Name:              yogaflow-backend
   Region:            Singapore
   Branch:            main
   Root Directory:    backend
   Runtime:           Python 3
   Build Command:     pip install -r requirements.txt
   Start Command:     uvicorn main:app --host 0.0.0.0 --port $PORT
   Instance Type:     Free
   ```

4. Click **"Create Web Service"**

5. **Wait for deployment** (~5-10 minutes)
   - Watch the logs for progress
   - Wait until status shows: **"Live"** ✅

6. **COPY Backend URL** (example: `https://yogaflow-backend.onrender.com`)
   - Save this URL, you'll need it later!

### 2.3 Test Backend

Open in browser: `https://yogaflow-backend.onrender.com`

You should see:
```json
{"status":"ok","model_loaded":true}
```

✅ **Backend deployed successfully!** Let's move to frontend.

---

## 🌐 STEP 3: Update API URL in Frontend

Before deploying frontend, we need to update the API URL.

### 3.1 Edit File

**File:** `frontend/components/yoga/hooks/useYogaSession.ts`

**Line 6**, change from:
```typescript
const API_URL = "http://localhost:8000/classify";
```

**To:**
```typescript
const API_URL = "https://yogaflow-backend.onrender.com/classify";
```

> ⚠️ Replace `yogaflow-backend.onrender.com` with your actual backend URL!

### 3.2 Commit & Push

```bash
git add frontend/components/yoga/hooks/useYogaSession.ts
git commit -m "Update API URL for production"
git push origin main
```

---

## 🌐 STEP 4: Deploy Frontend to Vercel

### 4.1 Create Account & Login

1. Go to https://vercel.com
2. Click **"Sign Up"**
3. Sign up with **GitHub**
4. Authorize Vercel

### 4.2 Deploy Frontend

1. In Vercel dashboard, click **"Add New..."** → **"Project"**

2. **Import Repository:**
   - Search: `ve11yn/yoga-pose-correction`
   - Click **"Import"**

3. **Configure Project:**
   ```
   Framework Preset:   Next.js
   Root Directory:     frontend
   Build Command:      (leave default)
   Output Directory:   (leave default)
   Install Command:    (leave default)
   ```

4. **Environment Variables:** (skip, leave empty)

5. Click **"Deploy"**

6. **Wait for deployment** (~2-3 minutes)
   - Watch progress in dashboard
   - Wait for the confetti 🎉

7. **COPY Frontend URL** (example: `https://yoga-pose-correction.vercel.app`)

---

## ✅ STEP 5: Testing

### 5.1 Test Backend

```bash
curl https://yogaflow-backend.onrender.com
```

Expected response:
```json
{"status":"ok","model_loaded":true}
```

### 5.2 Test Frontend

1. Open Vercel URL in browser
2. Click to enter **"Practice Mode"**
3. **Allow camera access** when prompted
4. Try a yoga pose → you should see:
   - ✅ Blue skeleton overlay on camera (mirrored)
   - ✅ Detected pose name
   - ✅ Correction feedback

---

## 🎉 DONE!

Your app is now live! 🚀

**Save your URLs:**
```
Frontend: https://yoga-pose-correction.vercel.app
Backend:  https://yogaflow-backend.onrender.com
GitHub:   https://github.com/ve11yn/yoga-pose-correction
```

---

## 🔄 Updating Your App

Whenever you make code changes:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

- **Vercel**: Auto deploys in ~2 minutes ⚡
- **Render**: Auto deploys in ~5-10 minutes 🔄

---

## ⚠️ Important Notes

### Render Free Tier

- ✅ **750 free hours/month** (enough for 24/7 for one month)
- ⚠️ **Cold start**: Server sleeps after 15 minutes of inactivity
  - First request after sleep: ~30 seconds
  - Subsequent requests: normal (~1-2 seconds)
  - **This is normal for free tier!**

### Vercel Free Tier

- ✅ **Unlimited** deployments
- ✅ **Auto HTTPS** (required for camera access)
- ✅ **Auto deploy** from GitHub
- ✅ **Fast** global CDN

---

## 🐛 Troubleshooting

### ❌ Backend: Model not loaded

**Error:** `{"status":"ok","model_loaded":false}`

**Solution:**
1. Check that `model/` folder exists in root project
2. Check that `svm_classifier.pkl` file exists in `model/` folder
3. View logs in Render dashboard for error details

### ❌ Frontend: Cannot connect to backend

**Error:** CORS error or network error in console

**Solution:**
1. Make sure API_URL is changed to Render URL (not localhost)
2. Make sure backend is running (open backend URL in browser)
3. Check CORS settings in `backend/main.py` (already allows all origins)

### ❌ Camera: Access denied

**Error:** "Camera access denied" or "NotAllowedError"

**Solution:**
1. Make sure you're using HTTPS (Vercel auto-provides HTTPS ✅)
2. Click "Allow" when browser asks for permission
3. Try a different browser (Chrome recommended)
4. Check browser settings → Site permissions → Camera

### ❌ Backend: Slow first request

**This is normal!** Render free tier sleeps after 15 minutes of inactivity.
- First request: ~30 seconds (server waking up)
- Subsequent requests: normal speed

**Solutions (optional):**
- Upgrade to paid plan ($7/month) for no sleep
- Or just accept it, it's fine for demo/portfolio

---

## 💰 Cost Summary

| Service | Plan | Limit | Cost |
|---------|------|-------|------|
| Vercel | Hobby | Unlimited | **$0** ✅ |
| Render | Free | 750 hours/month | **$0** ✅ |
| **TOTAL** | | | **$0/month** 🎉 |

---

## 🎓 Optional: Custom Domain

Want to use your own domain? (e.g., `yogaflow.com`)

**Vercel:**
1. Buy a domain (Namecheap, GoDaddy, etc.)
2. In Vercel dashboard → Settings → Domains
3. Add domain & follow DNS instructions
4. **Free!** (only pay for domain ~$10/year)

**Render:**
- Requires upgrade to paid plan ($7/month)

---

**Happy Deploying! 🚀**

Need help? Check logs in Render/Vercel dashboard or ask in GitHub Issues.
