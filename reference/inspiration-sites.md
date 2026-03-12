# Auto Spares E-commerce - Inspiration Sites Reference

This document catalogs design and feature inspiration from various auto parts e-commerce sites for the Kirinyaga auto spares project.

![Client Structure Notes](/home/maskgod/Documents/FRONT_END_WEB_DEVELOPMENT_COURSE/AUTOSPARES/reference/client-images/structure-notes.png)

---

## 1. Maridady Motors
**URL**: https://www.maridadymotors.com/

### 🎯 What We're Taking

#### Contact Section (Top Bar)
**Priority: HIGH** - First thing users see

The site has a prominent contact bar at the very top with:
- Phone: 0709-888-777
- Email: info@maridadymotors.com
- WhatsApp link
- Social Media Icons: Facebook, Instagram, Twitter

**Implementation Notes:**
- Icons displayed in a horizontal line
- Always visible at the top
- Clean, accessible layout
- Multiple contact options for customer convenience

#### Categories with Hover Effects
**Priority: MEDIUM**

Categories displayed in a line that show:
- Hover effects revealing more information
- Max posts count per category
- Clean category organization

**Features to Implement:**
- Filter by popular brands
- Filter by top ten popular cars
- Budget-based filtering
- 4WD & SUVs categorization

---

## 2. PartsPoa
**URL**: https://www.partspoa.com/

### 🎯 What We're Taking

#### Hot Deals Section
**Priority: HIGH**

Dedicated "Hot Deals" section featuring:
- AUTO PARTS UP TO 50% OFF promotions
- Quick access to discounted items
- Visual emphasis on savings

#### Quick Categories
**Priority: HIGH**

Clean category grid with "shop now" buttons:
- Body Parts
- Exterior Accessories
- Replacement Parts
- Tire and Wheels
- Interior Accessories
- Suspension & Performance
- Hot Deals (as a category)
- Engine & Components

**Implementation Notes:**
- Each category has a clear "shop now" CTA
- Easy navigation structure
- Visual category cards

#### Category Filtering System
**Priority: HIGH**

Advanced filtering by:
- **Car Make** (Brand)
- **Model**
- **Year**

**Sub-categories visible:**
- Extensive nested categories (e.g., Body Parts → Battery, Bonnet, Boot, Bumper, etc.)
- Deep product organization
- Easy drill-down navigation

#### Features
- My Basket / Checkout
- Wishlist / Saved Items
- Login / Register
- Customer Support link
- Free Shipping + 30-day return + 24/7 support

---

## 3. Amex Auto Parts
**URL**: https://amexautoparts.com/

### 🎯 What We're Taking

#### Image Banner with Moving Auto Specialists
**Priority: HIGH**

Hero/banner section featuring:
- Moving/animated elements
- "Auto specialists" messaging
- Visual appeal and engagement

#### Quick Categories with Icons
**Priority: HIGH**

Icon-based category navigation:
- Cooling Parts
- Lighting
- Body Parts
- Accessories
- Mirrors
- Ex Japan (products)

**Implementation Notes:**
- Visual icons for each category
- Clean, modern design
- Easy recognition

#### Search with Icon at Left
**Priority: MEDIUM**

Search functionality featuring:
- Search icon positioned at the left
- Easy-to-find search bar
- Prominent placement

#### Category Structure
When clicked, each category reveals:
- Detailed subcategories
- Organized filtering (Make, Model, Year)
- Easy navigation through parts

**Example from Lighting category:**
- Back Lamp, Brake Lamp, Bumper Lamp, Corner Lamp
- Fog Lamp, Front Lamp, Head Lamp
- Indicator Lamp, License Lamp, etc.

#### Top Bar Features
- Customer Care: 0753 300400
- Stores link
- Contacts link
- Shopping basket

---

## 4. James Edition
**URL**: https://www.jamesedition.com/

### 🎯 What We're Taking

#### Hero Section: Moving, Cinematic Cars
**Priority: HIGHEST**

**Note:** Site returned 403 error when attempting to access, but client notes indicate:
- Whole page with moving, cinematic cars
- Premium, luxury aesthetic
- Animated/video hero section
- High-end visual presentation

**Implementation Strategy:**
- Create cinematic hero with video or animated elements
- Showcase premium auto parts in elegant presentation
- Use smooth transitions and animations
- High-quality imagery

---

## Implementation Priority Summary

### Phase 1 - Essential Features
1. **Contact Section** (Maridady style)
   - Social media icons in line at top
   - Phone, Email, WhatsApp integration

2. **Hero Section** (James Edition inspiration)
   - Cinematic, moving cars
   - Premium visual design
   - Animated elements

3. **Quick Categories** (PartsPoa + Amex)
   - Icon-based categories
   - Clear "shop now" CTAs
   - Body Parts, Lighting, Accessories, etc.

### Phase 2 - Product Discovery
4. **Search Functionality** (Amex style)
   - Icon at left
   - Filter by Make, Model, Year
   - Advanced search options

5. **Hot Deals Section** (PartsPoa)
   - Dedicated deals page
   - Promotional badges
   - % off indicators

### Phase 3 - Enhanced Features
6. **Category Hover Effects** (Maridady)
   - Product count on hover
   - Smooth animations
   - Enhanced UX

7. **Footer & Support**
   - Customer support links
   - Company info
   - Policies and terms

---

## Design Aesthetic Goals

Based on all four sites, the design should be:
- **Modern**: Clean, contemporary design
- **Accessible**: Easy navigation, clear CTAs
- **Visual**: Icon-based categories, high-quality images
- **Premium**: Cinematic elements, smooth animations
- **Functional**: Smart filtering, quick access to products
- **Trustworthy**: Multiple contact options, support visible

---

## Technical Features to Implement

1. **Multi-channel Contact Integration**
   - WhatsApp Business API
   - Social media links
   - Email contact forms
   - Phone click-to-call

2. **Product Filtering System**
   - Filter by Make (Toyota, Nissan, Honda, etc.)
   - Filter by Model
   - Filter by Year
   - Category filtering

3. **E-commerce Functionality**
   - Shopping cart/basket
   - Wishlist
   - User accounts
   - Checkout process

4. **Visual Elements**
   - Animated hero section
   - Category icons
   - Product image galleries
   - Promotional badges

---

## Questions for Discussion

1. **Product Inventory**: How many products will we start with? Should we focus on specific categories first (e.g., Body Parts, Lighting)?

2. **Payment Integration**: What payment methods are most common in Kirinyaga? (M-Pesa, Cash on Delivery, Bank Transfer?)

3. **Delivery**: Will you offer delivery? What areas will you cover?

4. **Hero Section**: For the cinematic cars section, should we use:
   - Video background?
   - Animated images carousel?
   - Static premium images with animation effects?

5. **Contact Priority**: Which contact method is most important for your customers? (WhatsApp seems popular in Kenya)

6. **Product Data**: Do you have product catalogs with:
   - Product names
   - Images
   - Prices
   - Compatible makes/models?

---

## Next Steps

Once we discuss the questions above, we'll:
1. Create detailed wireframes for each section
2. Define the exact feature set for Phase 1
3. Set up the project structure
4. Begin development with the priority features
