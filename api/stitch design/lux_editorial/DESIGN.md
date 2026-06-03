---
name: Lux Editorial
colors:
  surface: '#fbf8fc'
  surface-dim: '#dbd9dd'
  surface-bright: '#fbf8fc'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f6'
  surface-container: '#efedf1'
  surface-container-high: '#eae7eb'
  surface-container-highest: '#e4e2e5'
  on-surface: '#1b1b1e'
  on-surface-variant: '#43474b'
  inverse-surface: '#303033'
  inverse-on-surface: '#f2f0f3'
  outline: '#74777c'
  outline-variant: '#c3c7cc'
  surface-tint: '#50606e'
  primary: '#475764'
  on-primary: '#ffffff'
  primary-container: '#5f6f7d'
  on-primary-container: '#e5f2ff'
  inverse-primary: '#b8c8d8'
  secondary: '#5f5f4f'
  on-secondary: '#ffffff'
  secondary-container: '#e2e1cc'
  on-secondary-container: '#646353'
  tertiary: '#465762'
  on-tertiary: '#ffffff'
  tertiary-container: '#5e6f7b'
  on-tertiary-container: '#e2f2ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d4e5f5'
  primary-fixed-dim: '#b8c8d8'
  on-primary-fixed: '#0d1d29'
  on-primary-fixed-variant: '#394956'
  secondary-fixed: '#e5e3cf'
  secondary-fixed-dim: '#c9c7b4'
  on-secondary-fixed: '#1c1c10'
  on-secondary-fixed-variant: '#474839'
  tertiary-fixed: '#d3e5f3'
  tertiary-fixed-dim: '#b7c9d7'
  on-tertiary-fixed: '#0c1d27'
  on-tertiary-fixed-variant: '#394954'
  background: '#fbf8fc'
  on-background: '#1b1b1e'
  surface-variant: '#e4e2e5'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 72px
    fontWeight: '300'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-xl:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '400'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.3'
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 28px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: DM Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: DM Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-sm:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.0'
    letterSpacing: 0.1em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1440px
  gutter: 32px
  margin-desktop: 80px
  margin-tablet: 40px
  margin-mobile: 20px
  stack-sm: 16px
  stack-md: 32px
  stack-lg: 64px
---

## Brand & Style

This design system is built on the intersection of high-fashion editorial print and cinematic digital experiences. The brand personality is poised, quiet, and intentional, targeting a discerning audience that values white space as much as content. 

The visual style employs a sophisticated mix of **Modern Minimalism** and **Subtle Glassmorphism**. We move away from the flat, clinical nature of traditional SaaS layouts toward a more organic, layered approach. The "Atmospheric" aesthetic is achieved through depth—not via harsh outlines, but through light, shadow, and soft blurs that suggest a physical, high-end environment. The goal is to evoke a sense of calm, premium quality, and immersive focus.

## Colors

The palette is intentionally "off-white" and "muted-tonal." We strictly avoid #000000 and #FFFFFF to maintain a soft, cinematic eye-feel. 

- **Primary (Muted Slate):** Used for primary actions and structural emphasis. 
- **Secondary (Warm Ivory):** The foundational warmth of the design system, used for large surface areas to create a "paper-like" feel.
- **Tertiary (Fog Blue):** Used for subtle accents, highlights, and secondary interactive states.
- **Neutral (Muted Charcoal):** Reserved for high-contrast typography and iconography.

All colors should feel as though they are viewed through a soft-focus lens. Use the **Warm Pearl** (#F8F3E7) as the primary canvas color to give the UI a luxurious, tactile foundation.

## Typography

The typography in this design system emphasizes clarity and rhythmic balance. We utilize **Hanken Grotesk** for headings to provide a sharp, contemporary edge that feels "designed." For body copy, **DM Sans** offers an understated, low-contrast readability that doesn't distract from visual content.

Large display headings should be set with tight tracking (-0.02em) to create a "block" look characteristic of high-end magazines. Body text requires generous line-height (1.6) to ensure an airy, breathable reading experience. Labels and metadata should always use uppercase with tracking (+0.1em) to create a clear hierarchy between content and navigation.

## Layout & Spacing

The layout philosophy follows a **Fixed Grid with Immense Margins**. Content should never feel crowded. 

- **Grid:** A 12-column grid for desktop with 32px gutters. On mobile, transition to a 4-column grid.
- **Margins:** Large exterior margins (80px on desktop) are mandatory to frame the portfolio work like a gallery piece.
- **Vertical Rhythm:** Use the `stack-lg` (64px) unit for section transitions to maintain an unhurried, editorial flow. 

Avoid "filling" the screen; instead, center content within generous containers to focus the user's gaze toward the cinematic imagery.

## Elevation & Depth

This design system uses depth to indicate hierarchy without relying on harsh borders. 

1.  **Backdrop Blurs:** Utilize 12px to 20px Gaussian blurs for navigation bars and modal overlays. This creates a "frosted glass" effect that keeps the background imagery visible but non-distracting.
2.  **Layered Shadows:** Shadows are extra-diffused and low-opacity. Use a multi-step shadow approach: a sharp, very light inner shadow for definition, and a wide, soft outer shadow (Blur: 40px, Spread: -5px) tinted with the **Muted Slate** color at 8% opacity.
3.  **Tonal Transitions:** Depth is often communicated simply by moving from **Warm Pearl** (base) to **Soft Vanilla** (elevated surface).

## Shapes

The shape language is "Softly Geometric." All structural elements (cards, containers, inputs) use a base radius of 0.5rem (8px). 

For larger cinematic hero components or immersive image containers, use `rounded-xl` (1.5rem / 24px) to emphasize the "object-like" quality of the content. Buttons should remain consistently at 0.5rem to feel professional and sturdy, avoiding the "bubbly" look of pill shapes.

## Components

### Buttons
Primary buttons use the **Muted Slate** background with **Warm Ivory** text. Secondary buttons are ghost-style with a thin 1px border in **Soft Silver**. Hover states should trigger a "lift" (subtle shadow increase) and a background color shift to **Fog Blue**.

### Cards
Cards are the core of the portfolio. They feature a 1px border in **Pale Mist** (nearly invisible) and a soft layered shadow. On hover, the image within the card should scale slightly (1.05x) with a 500ms ease-out transition.

### Input Fields
Fields are minimalist: a bottom-border only or a very light tonal fill (**Pale Linen**). Labels should sit above the field in the **label-sm** typography style.

### Navigation
The header should be a floating glassmorphic bar. Use a backdrop-filter (blur: 15px) and a background of **Warm Pearl** at 70% opacity.

### Motion
All transitions must be cinematic. Avoid "snappy" animations. Use `cubic-bezier(0.2, 0.8, 0.2, 1)` for all transforms. Implement a staggered fade-in for page loads where elements appear to float into place.