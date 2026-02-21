# Branding Guide

Quick reference for staying on-brand when building on this template. Based on the Capgemini brand guidelines.

---

## Colours

| Name | Hex | Tailwind class | Usage |
|------|-----|----------------|-------|
| **Capgemini Blue** | `#0070AD` | `cap-blue` | Primary buttons, nav bar, key actions |
| **Vibrant Blue** | `#12ABDB` | `vibrant-blue` | Accents, focus rings, links, card borders |
| **Deep Purple** | `#2B0A3D` | `deep-purple` | Page headings, hero text |
| **Tech Red** | `#FF304C` | `tech-red` | Errors, delete actions, alerts |
| **Zest Green** | `#95E616` | `zest-green` | Success states, active indicators |
| **Gray** | `#ECECEC` | `cap-gray` | Neutral backgrounds, dividers |
| **White** | `#FFFFFF` | `white` | Page background, card background |

Each colour has shades from `50` to `900` (e.g. `bg-cap-blue-100`, `text-cap-blue-700`).

---

## Typography

- **Font family:** Ubuntu (loaded via Google Fonts), Verdana fallback
- **Tailwind class:** `font-brand` (applied globally on `<body>`)
- **Weights available:** Light (300), Regular (400), Medium (500), Bold (700)

| Element | Weight | Example class |
|---------|--------|---------------|
| Page headings | Bold | `text-2xl font-bold text-deep-purple` |
| Card headings | Semibold | `text-lg font-semibold text-cap-gray-800` |
| Body text | Regular | `text-cap-gray-500` |
| Labels | Medium | `text-sm font-medium text-cap-gray-600` |
| Nav links | Medium | `text-sm font-medium` |

---

## Component Classes

Pre-built utility classes defined in `frontend/src/style.css`:

```css
.btn            /* Base button: padding, rounded, transition */
.btn-primary    /* Capgemini Blue background, white text */
.btn-secondary  /* Gray background */
.btn-danger     /* Tech Red background, white text */
.card           /* White background, subtle border, rounded-xl, padding */
.input          /* Full-width input with Vibrant Blue focus ring */
```

### Usage examples

```html
<!-- Primary action -->
<button class="btn btn-primary">Save</button>

<!-- Destructive action -->
<button class="btn btn-danger">Delete</button>

<!-- Card container -->
<div class="card">
  <h2 class="text-lg font-semibold text-cap-gray-800">Title</h2>
  <p class="text-cap-gray-500">Description</p>
</div>

<!-- Form input -->
<input class="input" placeholder="Enter value..." />

<!-- Accent border on a card -->
<div class="card border-l-4 border-l-vibrant-blue">...</div>
```

---

## Do's and Don'ts

**Do:**
- Use generous white space -- the brand relies on clean, uncluttered layouts
- Use Capgemini Blue for primary actions and navigation
- Use Deep Purple for page-level headings
- Use Vibrant Blue for interactive accents (links, focus states, highlights)
- Keep cards white with subtle borders

**Don't:**
- Introduce new brand colours outside this palette
- Use heavy drop shadows or dark backgrounds
- Mix more than 2-3 brand colours in a single component
- Use fonts other than Ubuntu / Verdana

---

## Files

| File | What it controls |
|------|-----------------|
| `frontend/tailwind.config.js` | Colour palette definitions, font family |
| `frontend/src/style.css` | Component classes (`.btn`, `.card`, `.input`) |
| `frontend/index.html` | Google Fonts import |

For the full brand guidelines, see the Capgemini Brand Guidelines PDF.
