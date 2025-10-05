# GitHub Pages Microsite Setup

This repository has been configured to serve as a GitHub Pages microsite showcasing the Marine Cable DAS Data Analysis & Maritime Surveillance Architecture documentation.

## 🚀 Quick Setup

### 1. Enable GitHub Pages
1. Go to your repository settings on GitHub
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "Deploy from a branch"
4. Choose "gh-pages" branch and "/ (root)" folder
5. Click "Save"

### 2. Create gh-pages Branch
```bash
# Create and switch to gh-pages branch
git checkout -b gh-pages

# Add all files
git add .

# Commit changes
git commit -m "Initial GitHub Pages setup"

# Push to GitHub
git push origin gh-pages
```

### 3. Access Your Site
Your microsite will be available at:
`https://<your-username>.github.io/undersea-cable/`

## 📁 Site Structure

```
/
├── _config.yml          # Jekyll configuration
├── _layouts/            # HTML templates
├── assets/css/          # Custom styling
├── index.md             # Homepage
├── *.md                 # Root-level documentation
├── analysis/            # Analysis documentation
│   ├── index.md         # Analysis homepage
│   ├── *.md            # Analysis documents
│   └── artifacts/       # Analysis results and visualizations
└── Gemfile             # Jekyll dependencies
```

## 📋 Content Organization

### Root Level Documents
- **index.md** - Homepage with navigation
- **EXECUTIVE_SUMMARY.md** - Business case and financial projections
- **ARCHITECTURE_DECISION_SUMMARY.md** - Technical architecture quick reference
- **ENGINEERING_DISCUSSION_GUIDE.md** - Technical validation questions
- **COMPRESSION_EVENT_DETECTION_SUMMARY.md** - Key findings summary
- **DAS_MARITIME_ARCHITECTURE.md** - GPU-at-edge architecture
- **DAS_CPU_ARCHITECTURE_ALTERNATIVE.md** - CPU-based architecture
- **DAS_TECHNICAL_IMPLEMENTATION.md** - Implementation details
- **INFORMATION_THEORY_ANALYSIS.md** - Mathematical analysis
- **DAS_BUSINESS_STRATEGY.md** - Market analysis and strategy

### Analysis Section
- **analysis/index.md** - Analysis documentation homepage
- **analysis/COMPRESSION_EVENT_DETECTION.md** - Complete technical analysis
- **analysis/RESULTS.md** - Detailed findings
- **analysis/SOLUTION_SUMMARY.md** - Problem-solving documentation
- **analysis/artifacts/** - Analysis results, visualizations, and data files

## 🎨 Customization

### Styling
- Edit `assets/css/style.css` to customize appearance
- Colors and fonts defined in CSS variables at the top of the file

### Navigation
- Update `_config.yml` navigation section to modify menu items
- Add new pages by creating `.md` files with proper front matter

### Content
- All markdown files include Jekyll front matter for proper rendering
- Images and visualizations are automatically included
- Tables, code blocks, and mathematical expressions are supported

## 🔧 Local Development

### Prerequisites
- Ruby 2.7 or higher
- Bundler gem

### Setup
```bash
# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve

# Access at http://localhost:4000
```

### Build
```bash
# Build static site
bundle exec jekyll build

# Output in _site/ directory
```

## 📊 Key Features

### Responsive Design
- Mobile-friendly layout
- Print-optimized styles
- Accessible navigation

### SEO Optimized
- Meta tags and Open Graph support
- Sitemap generation
- RSS feed support

### Content Management
- Automatic navigation generation
- Relative link support
- Collection-based organization

## 🚀 Deployment

### Automatic Deployment
GitHub Pages automatically rebuilds the site when you push changes to the `gh-pages` branch.

### Manual Deployment
```bash
# Make changes to content
git add .
git commit -m "Update documentation"
git push origin gh-pages
```

## 📈 Analytics & Monitoring

### Built-in Features
- Jekyll sitemap for search engine indexing
- RSS feed for content updates
- Social media meta tags

### Optional Additions
- Google Analytics (add tracking code to `_layouts/default.html`)
- GitHub Pages analytics (enable in repository settings)

## 🛠️ Troubleshooting

### Common Issues
1. **Site not updating**: Check GitHub Pages build status in repository settings
2. **Missing images**: Ensure image paths are relative and files are committed
3. **Broken links**: Use Jekyll's `relative_url` filter for internal links
4. **Styling issues**: Check CSS file is properly linked in layout

### Build Errors
- Check Jekyll build logs in GitHub Actions
- Validate YAML syntax in `_config.yml`
- Ensure all markdown files have proper front matter

## 📞 Support

For issues with the microsite setup:
1. Check GitHub Pages documentation
2. Review Jekyll configuration
3. Validate markdown syntax
4. Check file permissions and paths

---

*This microsite showcases comprehensive documentation for DAS maritime surveillance technology, including technical architecture, business strategy, and empirical analysis results.*
