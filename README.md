# Capitalmind studio case study

A one-page website version of Vikas Banjare's production case study for the Capitalmind Studio Lead – Video Production role: five findings from 60 @CapitalmindHQ videos, the brand-recognition plan, how the studio would run, a merged 90-day plan, experience, and a sortable log of all 60 videos.

## Run it

It's a static site. Open `index.html` directly, or serve the folder:

```sh
npx http-server .
```

## Edit it

- Page source: `src/template.html`
- Video data (appendix table): `src/videos.json`
- Images: `assets/img/`, fonts: `assets/fonts/`, logo: `assets/logo.svg`

After editing, rebuild `index.html` (inlines the logo, fonts and data):

```sh
python3 src/build.py
```
