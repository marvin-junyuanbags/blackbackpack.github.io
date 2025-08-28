#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate SVG images for backpack-design-trends-innovations-2024.html article
This script creates all the missing SVG images referenced in the article.
"""

import os

def create_svg_content(title, description, icon_type="tech"):
    """
    Create SVG content based on the image type and description
    """
    
    # Color schemes for different types
    color_schemes = {
        "tech": {"primary": "#2563eb", "secondary": "#1e40af", "accent": "#3b82f6"},
        "sustainable": {"primary": "#059669", "secondary": "#047857", "accent": "#10b981"},
        "design": {"primary": "#7c3aed", "secondary": "#6d28d9", "accent": "#8b5cf6"},
        "ergonomic": {"primary": "#dc2626", "secondary": "#b91c1c", "accent": "#ef4444"},
        "functional": {"primary": "#ea580c", "secondary": "#c2410c", "accent": "#f97316"},
        "aesthetic": {"primary": "#be185d", "secondary": "#9d174d", "accent": "#ec4899"}
    }
    
    colors = color_schemes.get(icon_type, color_schemes["tech"])
    
    # Base SVG template
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors['primary']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{colors['secondary']};stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{colors['accent']};stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:{colors['primary']};stop-opacity:0.8" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="300" fill="url(#grad1)" rx="10" ry="10"/>
  
  <!-- Main content area -->
  <rect x="20" y="20" width="360" height="260" fill="rgba(255,255,255,0.1)" rx="8" ry="8" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
'''
    
    # Add specific icons based on the title/description
    if "smart" in title.lower() or "wireless" in title.lower() or "gps" in title.lower():
        # Tech/Smart features
        svg_content += '''
  <!-- Smart device icon -->
  <rect x="50" y="60" width="80" height="120" fill="rgba(255,255,255,0.9)" rx="8" ry="8"/>
  <circle cx="90" cy="80" r="8" fill="url(#grad2)"/>
  <rect x="70" y="100" width="40" height="4" fill="url(#grad2)" rx="2"/>
  <rect x="70" y="110" width="30" height="4" fill="url(#grad2)" rx="2"/>
  <rect x="70" y="120" width="35" height="4" fill="url(#grad2)" rx="2"/>
  
  <!-- Connection lines -->
  <path d="M 130 120 Q 180 100 230 120" stroke="rgba(255,255,255,0.8)" stroke-width="2" fill="none"/>
  <path d="M 130 140 Q 180 160 230 140" stroke="rgba(255,255,255,0.8)" stroke-width="2" fill="none"/>
  
  <!-- Secondary elements -->
  <circle cx="250" cy="120" r="15" fill="rgba(255,255,255,0.9)"/>
  <circle cx="250" cy="140" r="15" fill="rgba(255,255,255,0.9)"/>
  <circle cx="320" cy="130" r="20" fill="rgba(255,255,255,0.9)"/>
'''
    elif "sustainable" in title.lower() or "eco" in title.lower() or "recycled" in title.lower() or "bio" in title.lower():
        # Sustainable/Eco features
        svg_content += '''
  <!-- Leaf/Nature icon -->
  <path d="M 100 80 Q 120 60 140 80 Q 160 100 140 120 Q 120 140 100 120 Q 80 100 100 80" fill="rgba(255,255,255,0.9)"/>
  <path d="M 100 80 Q 110 90 120 100 Q 130 110 140 120" stroke="url(#grad2)" stroke-width="3" fill="none"/>
  
  <!-- Recycling arrows -->
  <g transform="translate(200,100)">
    <path d="M 0 -20 A 20 20 0 0 1 17.32 10 L 10 15 L 20 5 L 15 -5 A 20 20 0 0 1 0 -20" fill="rgba(255,255,255,0.9)"/>
    <path d="M 17.32 10 A 20 20 0 0 1 -17.32 10 L -10 15 L -20 5 L -15 -5 A 20 20 0 0 1 17.32 10" fill="rgba(255,255,255,0.9)"/>
    <path d="M -17.32 10 A 20 20 0 0 1 0 -20 L -10 -15 L 0 -25 L 10 -15 A 20 20 0 0 1 -17.32 10" fill="rgba(255,255,255,0.9)"/>
  </g>
  
  <!-- Earth/Globe -->
  <circle cx="300" cy="120" r="30" fill="rgba(255,255,255,0.9)"/>
  <path d="M 280 120 Q 300 100 320 120 Q 300 140 280 120" fill="url(#grad2)"/>
  <path d="M 290 110 Q 300 115 310 110" stroke="url(#grad2)" stroke-width="2" fill="none"/>
  <path d="M 290 130 Q 300 125 310 130" stroke="url(#grad2)" stroke-width="2" fill="none"/>
'''
    elif "modular" in title.lower() or "expandable" in title.lower() or "convertible" in title.lower():
        # Modular/Flexible features
        svg_content += '''
  <!-- Modular blocks -->
  <rect x="60" y="80" width="40" height="40" fill="rgba(255,255,255,0.9)" rx="4"/>
  <rect x="110" y="80" width="40" height="40" fill="rgba(255,255,255,0.7)" rx="4"/>
  <rect x="160" y="80" width="40" height="40" fill="rgba(255,255,255,0.9)" rx="4"/>
  
  <rect x="60" y="130" width="40" height="40" fill="rgba(255,255,255,0.7)" rx="4"/>
  <rect x="110" y="130" width="40" height="40" fill="rgba(255,255,255,0.9)" rx="4"/>
  <rect x="160" y="130" width="40" height="40" fill="rgba(255,255,255,0.7)" rx="4"/>
  
  <!-- Connection points -->
  <circle cx="105" cy="100" r="3" fill="url(#grad2)"/>
  <circle cx="155" cy="100" r="3" fill="url(#grad2)"/>
  <circle cx="80" cy="125" r="3" fill="url(#grad2)"/>
  <circle cx="130" cy="125" r="3" fill="url(#grad2)"/>
  <circle cx="180" cy="125" r="3" fill="url(#grad2)"/>
  
  <!-- Arrows showing flexibility -->
  <path d="M 220 100 L 250 100 L 245 95 M 250 100 L 245 105" stroke="rgba(255,255,255,0.8)" stroke-width="2" fill="none"/>
  <path d="M 250 120 L 220 120 L 225 115 M 220 120 L 225 125" stroke="rgba(255,255,255,0.8)" stroke-width="2" fill="none"/>
  
  <!-- Result configuration -->
  <rect x="270" y="90" width="60" height="60" fill="rgba(255,255,255,0.9)" rx="6"/>
  <rect x="280" y="100" width="15" height="15" fill="url(#grad2)" rx="2"/>
  <rect x="300" y="100" width="15" height="15" fill="url(#grad2)" rx="2"/>
  <rect x="320" y="100" width="15" height="15" fill="url(#grad2)" rx="2"/>
  <rect x="280" y="120" width="15" height="15" fill="url(#grad2)" rx="2"/>
  <rect x="300" y="120" width="15" height="15" fill="url(#grad2)" rx="2"/>
  <rect x="320" y="120" width="15" height="15" fill="url(#grad2)" rx="2"/>
'''
    elif "ergonomic" in title.lower() or "posture" in title.lower() or "adaptive" in title.lower() or "suspension" in title.lower():
        # Ergonomic/Health features
        svg_content += '''
  <!-- Human figure -->
  <g transform="translate(80,60)">
    <circle cx="20" cy="20" r="12" fill="rgba(255,255,255,0.9)"/>
    <rect x="15" y="32" width="10" height="40" fill="rgba(255,255,255,0.9)" rx="5"/>
    <rect x="10" y="40" width="8" height="25" fill="rgba(255,255,255,0.7)" rx="4"/>
    <rect x="22" y="40" width="8" height="25" fill="rgba(255,255,255,0.7)" rx="4"/>
    <rect x="12" y="72" width="6" height="30" fill="rgba(255,255,255,0.7)" rx="3"/>
    <rect x="22" y="72" width="6" height="30" fill="rgba(255,255,255,0.7)" rx="3"/>
  </g>
  
  <!-- Backpack outline -->
  <rect x="95" y="80" width="25" height="50" fill="url(#grad2)" rx="8"/>
  <rect x="98" y="85" width="19" height="8" fill="rgba(255,255,255,0.3)" rx="2"/>
  <rect x="98" y="95" width="19" height="8" fill="rgba(255,255,255,0.3)" rx="2"/>
  <rect x="98" y="105" width="19" height="8" fill="rgba(255,255,255,0.3)" rx="2"/>
  
  <!-- Pressure distribution lines -->
  <g stroke="rgba(255,255,255,0.8)" stroke-width="2" fill="none">
    <path d="M 140 90 Q 160 85 180 90"/>
    <path d="M 140 100 Q 160 95 180 100"/>
    <path d="M 140 110 Q 160 105 180 110"/>
    <path d="M 140 120 Q 160 115 180 120"/>
  </g>
  
  <!-- Comfort indicators -->
  <circle cx="200" cy="90" r="8" fill="rgba(255,255,255,0.9)"/>
  <circle cx="200" cy="110" r="8" fill="rgba(255,255,255,0.9)"/>
  <circle cx="200" cy="130" r="8" fill="rgba(255,255,255,0.9)"/>
  
  <!-- Spine alignment guide -->
  <path d="M 250 70 Q 260 90 250 110 Q 240 130 250 150" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none"/>
  <circle cx="250" cy="70" r="4" fill="rgba(255,255,255,0.9)"/>
  <circle cx="250" cy="90" r="4" fill="rgba(255,255,255,0.9)"/>
  <circle cx="250" cy="110" r="4" fill="rgba(255,255,255,0.9)"/>
  <circle cx="250" cy="130" r="4" fill="rgba(255,255,255,0.9)"/>
  <circle cx="250" cy="150" r="4" fill="rgba(255,255,255,0.9)"/>
'''
    elif "climate" in title.lower() or "water" in title.lower() or "emergency" in title.lower() or "auto" in title.lower():
        # Functional/Technical features
        svg_content += '''
  <!-- Control panel -->
  <rect x="60" y="70" width="100" height="80" fill="rgba(255,255,255,0.9)" rx="8"/>
  <rect x="70" y="80" width="80" height="8" fill="url(#grad2)" rx="4"/>
  <rect x="70" y="95" width="60" height="8" fill="url(#grad2)" rx="4"/>
  <rect x="70" y="110" width="70" height="8" fill="url(#grad2)" rx="4"/>
  
  <!-- Buttons/Controls -->
  <circle cx="80" cy="130" r="6" fill="url(#grad2)"/>
  <circle cx="100" cy="130" r="6" fill="url(#grad2)"/>
  <circle cx="120" cy="130" r="6" fill="url(#grad2)"/>
  <circle cx="140" cy="130" r="6" fill="url(#grad2)"/>
  
  <!-- System diagram -->
  <g transform="translate(200,80)">
    <rect x="0" y="0" width="60" height="40" fill="rgba(255,255,255,0.9)" rx="6"/>
    <rect x="10" y="10" width="40" height="4" fill="url(#grad2)" rx="2"/>
    <rect x="10" y="18" width="30" height="4" fill="url(#grad2)" rx="2"/>
    <rect x="10" y="26" width="35" height="4" fill="url(#grad2)" rx="2"/>
    
    <!-- Flow arrows -->
    <path d="M 30 45 L 30 65 L 25 60 M 30 65 L 35 60" stroke="rgba(255,255,255,0.8)" stroke-width="2" fill="none"/>
    
    <!-- Output indicator -->
    <rect x="10" y="70" width="40" height="20" fill="rgba(255,255,255,0.7)" rx="4"/>
    <circle cx="30" cy="80" r="6" fill="url(#grad2)"/>
  </g>
  
  <!-- Status indicators -->
  <circle cx="300" cy="90" r="8" fill="#10b981"/>
  <circle cx="320" cy="90" r="8" fill="#f59e0b"/>
  <circle cx="340" cy="90" r="8" fill="#ef4444"/>
'''
    elif "aesthetic" in title.lower() or "design" in title.lower() or "minimalist" in title.lower() or "retro" in title.lower() or "nature" in title.lower():
        # Aesthetic/Design features
        svg_content += '''
  <!-- Design elements -->
  <g transform="translate(80,80)">
    <!-- Geometric shapes -->
    <polygon points="40,20 60,40 40,60 20,40" fill="rgba(255,255,255,0.9)"/>
    <circle cx="100" cy="40" r="20" fill="rgba(255,255,255,0.7)"/>
    <rect x="140" y="20" width="40" height="40" fill="rgba(255,255,255,0.9)" rx="8"/>
    
    <!-- Pattern lines -->
    <g stroke="url(#grad2)" stroke-width="2" fill="none">
      <path d="M 200 20 L 240 60"/>
      <path d="M 200 60 L 240 20"/>
      <path d="M 220 20 L 220 60"/>
      <path d="M 200 40 L 240 40"/>
    </g>
  </g>
  
  <!-- Color palette -->
  <g transform="translate(60,160)">
    <rect x="0" y="0" width="30" height="30" fill="#1f2937" rx="4"/>
    <rect x="35" y="0" width="30" height="30" fill="#6b7280" rx="4"/>
    <rect x="70" y="0" width="30" height="30" fill="#d1d5db" rx="4"/>
    <rect x="105" y="0" width="30" height="30" fill="#f9fafb" rx="4"/>
    <rect x="140" y="0" width="30" height="30" fill="url(#grad2)" rx="4"/>
  </g>
  
  <!-- Style indicators -->
  <g transform="translate(250,140)">
    <path d="M 0 0 Q 20 -10 40 0 Q 60 10 80 0" stroke="rgba(255,255,255,0.8)" stroke-width="3" fill="none"/>
    <path d="M 0 20 L 80 20" stroke="rgba(255,255,255,0.8)" stroke-width="3"/>
    <path d="M 0 40 Q 40 30 80 40" stroke="rgba(255,255,255,0.8)" stroke-width="3" fill="none"/>
  </g>
'''
    else:
        # Default/Generic features
        svg_content += '''
  <!-- Generic backpack icon -->
  <rect x="120" y="60" width="60" height="80" fill="rgba(255,255,255,0.9)" rx="12"/>
  <rect x="130" y="70" width="40" height="10" fill="url(#grad2)" rx="2"/>
  <rect x="130" y="85" width="40" height="10" fill="url(#grad2)" rx="2"/>
  <rect x="130" y="100" width="40" height="10" fill="url(#grad2)" rx="2"/>
  
  <!-- Straps -->
  <rect x="110" y="70" width="8" height="60" fill="rgba(255,255,255,0.7)" rx="4"/>
  <rect x="182" y="70" width="8" height="60" fill="rgba(255,255,255,0.7)" rx="4"/>
  
  <!-- Features indicators -->
  <circle cx="200" cy="80" r="12" fill="rgba(255,255,255,0.9)"/>
  <circle cx="220" cy="100" r="12" fill="rgba(255,255,255,0.9)"/>
  <circle cx="200" cy="120" r="12" fill="rgba(255,255,255,0.9)"/>
  
  <!-- Connection lines -->
  <path d="M 180 90 L 188 85" stroke="rgba(255,255,255,0.8)" stroke-width="2"/>
  <path d="M 180 100 L 208 100" stroke="rgba(255,255,255,0.8)" stroke-width="2"/>
  <path d="M 180 110 L 188 115" stroke="rgba(255,255,255,0.8)" stroke-width="2"/>
'''
    
    # Add title text
    svg_content += f'''
  <!-- Title text -->
  <text x="200" y="250" text-anchor="middle" fill="rgba(255,255,255,0.95)" font-family="Arial, sans-serif" font-size="16" font-weight="bold">{title}</text>
  <text x="200" y="270" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-family="Arial, sans-serif" font-size="12">{description}</text>
</svg>'''
    
    return svg_content

def main():
    # Create images directory if it doesn't exist
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    # Define all SVG images needed for the article
    svg_images = {
        # Smart Technology Integration
        "innovative-backpack-design.svg": ("Innovative Design", "2024 Backpack Innovations", "design"),
        "wireless-charging-backpack.svg": ("Wireless Charging", "Built-in Power Solutions", "tech"),
        "gps-tracking-backpack.svg": ("GPS Tracking", "Location & Security", "tech"),
        "smart-organization-system.svg": ("Smart Organization", "Intelligent Compartments", "tech"),
        "biometric-security-backpack.svg": ("Biometric Security", "Advanced Protection", "tech"),
        "smart-backpack-adoption-stats.svg": ("Adoption Statistics", "Market Analysis 2024", "tech"),
        
        # Sustainable Design
        "recycled-ocean-plastic-material.svg": ("Ocean Plastic", "Recycled Materials", "sustainable"),
        "bio-based-materials.svg": ("Bio-Based Materials", "Sustainable Innovation", "sustainable"),
        "recycled-textile-fibers.svg": ("Recycled Textiles", "Circular Economy", "sustainable"),
        "design-for-disassembly.svg": ("Design for Disassembly", "Circular Design", "sustainable"),
        "durability-optimization.svg": ("Durability Focus", "Long-lasting Design", "sustainable"),
        "material-minimization.svg": ("Material Efficiency", "Waste Reduction", "sustainable"),
        
        # Modular Systems
        "modular-compartment-system.svg": ("Modular Compartments", "Flexible Organization", "modular"),
        "expandable-capacity-system.svg": ("Expandable Capacity", "Dynamic Volume", "modular"),
        "convertible-design-system.svg": ("Convertible Design", "Multi-Function", "modular"),
        "modular-design-benefits.svg": ("Design Benefits", "Market Advantages", "modular"),
        
        # Ergonomic Innovations
        "adaptive-suspension-system.svg": ("Adaptive Suspension", "Dynamic Load Distribution", "ergonomic"),
        "smart-weight-distribution.svg": ("Weight Distribution", "AI-Powered Balance", "ergonomic"),
        "breathable-back-panel.svg": ("Ventilation System", "Advanced Airflow", "ergonomic"),
        "posture-monitoring-system.svg": ("Posture Monitoring", "Health Tracking", "ergonomic"),
        
        # Aesthetic Trends
        "minimalist-design-trend.svg": ("Minimalist Design", "Clean Aesthetics", "aesthetic"),
        "retro-futuristic-design.svg": ("Retro-Futuristic", "Vintage Meets Future", "aesthetic"),
        "nature-inspired-design.svg": ("Nature Inspired", "Organic Forms", "aesthetic"),
        "urban-tactical-design.svg": ("Urban Tactical", "Technical Wear", "aesthetic"),
        
        # Advanced Functional Features
        "climate-control-system.svg": ("Climate Control", "Temperature Regulation", "functional"),
        "auto-organization-system.svg": ("Auto Organization", "Smart Compartments", "functional"),
        "water-purification-system.svg": ("Water Purification", "Built-in Filtration", "functional"),
        "emergency-communication-system.svg": ("Emergency Comm", "Safety Features", "functional"),
        "performance-enhancement-features.svg": ("Performance Features", "User Optimization", "functional"),
        
        # Sidebar and Footer Images
        "advanced-manufacturing-facility.svg": ("Manufacturing", "Advanced Techniques", "tech"),
        "sustainable-backpack-manufacturing.svg": ("Sustainable Mfg", "Eco-Friendly Production", "sustainable"),
        "backpack-materials-comparison.svg": ("Materials Guide", "Performance Comparison", "design"),
        "design-inspiration-icon.svg": ("Design Inspiration", "Creative Resources", "design"),
        "trend-forecast-icon.svg": ("Trend Forecast", "Future Predictions", "design"),
        "color-palette-icon.svg": ("Color Palettes", "Seasonal Colors", "aesthetic"),
        "logo.svg": ("Black Backpack", "Premium Manufacturing", "design")
    }
    
    print(f"Generating {len(svg_images)} SVG images...")
    
    for filename, (title, description, icon_type) in svg_images.items():
        filepath = os.path.join(images_dir, filename)
        
        # Generate SVG content
        svg_content = create_svg_content(title, description, icon_type)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"Created: {filepath}")
    
    print("\nAll SVG images generated successfully!")
    print(f"Images saved to: {os.path.abspath(images_dir)}")

if __name__ == "__main__":
    main()