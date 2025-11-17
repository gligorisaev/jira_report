# 🚀 Enable GitHub Pages

Follow these steps to make your dashboard accessible online:

## Step 1: Enable GitHub Pages

1. Go to your GitHub repository: https://github.com/gligorisaev/jira_report
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under "Source":
   - Select **Deploy from a branch**
   - Branch: **main**
   - Folder: **/docs**
5. Click **Save**

## Step 2: Wait for Deployment

GitHub will automatically deploy your site. This takes 1-2 minutes.

You'll see a message: "Your site is live at https://gligorisaev.github.io/jira_report/"

## Step 3: Access Your Dashboard

Once deployed, your dashboard will be available at:

**🌐 https://gligorisaev.github.io/jira_report/**

## What Happens

- Users can visit the URL directly
- They'll see the upload interface
- They can drag & drop their CSV file
- Dashboard generates instantly in their browser
- No server setup or hosting costs!

## Benefits

✅ **No Installation** - Works in any browser  
✅ **Always Available** - 24/7 access from anywhere  
✅ **Secure** - All processing happens client-side  
✅ **Free** - GitHub Pages is free for public repos  
✅ **Easy to Share** - Just send the URL  

## Update the Dashboard

To update the live dashboard:

```bash
# Make changes to index.html
# Copy to docs folder
Copy-Item index.html docs/app.html

# Commit and push
git add docs/
git commit -m "Update dashboard"
git push
```

GitHub Pages will automatically redeploy within 1-2 minutes.

## Troubleshooting

**Site not showing?**
- Wait 2-3 minutes after enabling Pages
- Check Settings → Pages for deployment status
- Make sure /docs folder is selected

**Changes not appearing?**
- GitHub Pages has a small cache
- Try clearing browser cache (Ctrl+F5)
- Wait a few minutes for redeployment

**404 Error?**
- Verify the /docs folder exists in your repository
- Check that app.html is in the docs folder
- Ensure GitHub Pages is enabled in settings
