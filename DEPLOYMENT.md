# 🚀 Deploy WorshipFlow AI to the Web

This guide will help you deploy WorshipFlow AI to Streamlit Cloud for free, making it accessible on the web.

## Option 1: Deploy to Streamlit Cloud (Recommended - FREE)

Streamlit Cloud offers free hosting for Streamlit apps with automatic deployment from GitHub.

### Step 1: Push to GitHub

1. **Create a new repository on GitHub**:
   - Go to [github.com](https://github.com)
   - Click the "+" icon and select "New repository"
   - Name it `worshipflow-ai` (or your preferred name)
   - Keep it Public (required for free Streamlit Cloud)
   - Don't initialize with README (we already have one)
   - Click "Create repository"

2. **Push your code to GitHub**:
   ```bash
   # Copy the commands from GitHub after creating the repo
   git remote add origin https://github.com/YOUR_USERNAME/worshipflow-ai.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Sign in with GitHub**

3. **Click "New app"**

4. **Configure your deployment**:
   - **Repository**: Select `worshipflow-ai`
   - **Branch**: `main`
   - **File path**: `worshipflow_ai.py`
   - **App settings** (optional):
     - URL: `worshipflow-ai`
     - App title: `WorshipFlow AI`
     - Icon: 🎵

5. **Add Environment Variables** (if using OpenAI):
   - Click "Advanced" → "Secrets"
   - Add: `OPENAI_API_KEY = "your-api-key-here"`

6. **Click "Deploy"**

7. **Wait for deployment** (usually 2-5 minutes)

8. **Your app is live!** You'll get a URL like:
   ```
   https://worshipflow-ai.streamlit.app
   ```

### Step 3: Share Your App

- Share the URL with your team or congregation
- The app is now accessible from any device with a web browser
- Updates are automatic when you push to GitHub

---

## Option 2: Deploy to Hugging Face Spaces (FREE)

Hugging Face Spaces also offers free hosting for Streamlit apps.

### Steps:

1. **Create a Hugging Face account** at [huggingface.co](https://huggingface.co)

2. **Create a new Space**:
   - Click your profile → "New Space"
   - Space name: `worshipflow-ai`
   - License: MIT
   - SDK: Streamlit
   - Visibility: Public

3. **Import from GitHub**:
   - Connect your GitHub account
   - Select the `worshipflow-ai` repository
   - Click "Import"

4. **Add Secrets** (if using OpenAI):
   - Go to Space Settings → Repository Secrets
   - Add `OPENAI_API_KEY`

5. **Your app will deploy automatically**

---

## Option 3: Deploy to Railway or Render (FREE tier)

These platforms offer free tiers with more resources.

### Railway:
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables
5. Deploy

### Render:
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your repository
4. Configure build and start commands:
   - Build: `pip install -r requirements.txt`
   - Start: `streamlit run worshipflow_ai.py --server.port $PORT --server.address 0.0.0.0`
5. Add environment variables
6. Deploy

---

## 📝 Post-Deployment Checklist

- [ ] Test the app in your browser
- [ ] Share the URL with your team
- [ ] Add OpenAI API key if you want AI features
- [ ] Bookmark the admin dashboard (Streamlit Cloud)
- [ ] Set up automatic updates from GitHub

---

## 🔧 Custom Domain (Optional)

### Streamlit Cloud:
- Custom domains require a paid plan
- Upgrade to Streamlit Cloud Pro for custom domain support

### Alternative - Use a URL shortener:
- Use Bitly or TinyURL to create a memorable link
- Example: `bit.ly/worshipflow-ai`

---

## 📊 Monitoring Your App

### Streamlit Cloud Dashboard:
- View usage statistics
- See deployment history
- Manage secrets and settings
- View error logs

---

## 🆘 Troubleshooting

### App won't deploy:
1. Check that `requirements.txt` is in the root directory
2. Ensure `worshipflow_ai.py` is the correct filename
3. Check deployment logs for errors
4. Verify all dependencies are listed in requirements.txt

### OpenAI not working:
1. Verify API key is correct
2. Check that the secret is named exactly `OPENAI_API_KEY`
3. Ensure your OpenAI account has credits

### App is slow:
- Free tiers have limited resources
- Consider upgrading to a paid plan for better performance
- Optimize the app by reducing database size

---

## 🎉 You're Live!

Your WorshipFlow AI app is now accessible on the web! Share it with your worship team, pastors, and other worship leaders.

**Example URL**: `https://worshipflow-ai.streamlit.app`

---

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Deployment Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

**Need help?** Open an issue on GitHub or contact support.