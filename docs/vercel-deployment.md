# Deploying to Vercel

## Prerequisites

1. GitHub Account
2. Vercel Account (can sign up with GitHub)
3. Repository cloned locally

## Automatic Deployment

### 1. Connect to Vercel

1. Go to [Vercel](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Select "Other" as framework preset

### 2. Configure Project

Vercel will automatically detect the MkDocs configuration. Use these settings:

- Build Command: `pip install -r requirements.txt && mkdocs build`
- Output Directory: `site`
- Install Command: `pip install -r requirements.txt`

## Manual Deployment

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

## Environment Variables

Add these in Vercel project settings if needed:

```bash
PYTHON_VERSION=3.9
NODE_VERSION=18.x
```

## Custom Domain

1. Go to project settings in Vercel
2. Click "Domains"
3. Add your domain
4. Configure DNS settings

## Troubleshooting

### Build Errors

1. Check Python version:
```bash
# Should be Python 3.9 or higher
python --version
```

2. Verify requirements:
```bash
# Install locally first
pip install -r requirements.txt

# Build locally
mkdocs build
```

3. Check build logs in Vercel

### Common Issues

1. **Build fails**: Make sure all dependencies are in `requirements.txt`

2. **404 errors**: Check `vercel.json` routes configuration

3. **Missing styles**: Verify `mkdocs.yml` theme configuration

## Monitoring

### Analytics

Add to `mkdocs.yml`:
```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

### Performance

Check Vercel Analytics for:
- Page load times
- Visitor statistics
- Error rates

## Maintenance

### Updates

1. Push changes to main branch
2. Vercel auto-deploys

### Preview Deployments

1. Create feature branch
2. Push changes
3. Vercel creates preview URL

## Best Practices

1. **Version Control**:
   - Keep dependencies updated
   - Use specific versions in requirements.txt

2. **Testing**:
   - Test locally before pushing
   - Use preview deployments

3. **Performance**:
   - Optimize images
   - Minimize custom JavaScript
   - Use recommended MkDocs settings

4. **SEO**:
   - Add meta descriptions
   - Use proper heading hierarchy
   - Include sitemap

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [GitHub Issues](https://github.com/ajeetraina/jetson-orin-nano-super-guide/issues)