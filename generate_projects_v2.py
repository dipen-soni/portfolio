import re
import urllib.request
import urllib.error
import socket
from urllib.parse import urlparse
import os

def parse_projects(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    chunks = content.split("Project")
    projects = []
    
    for chunk in chunks[1:]:
        chunk = chunk.strip()
        
        # Extract URL/Name
        url_match = re.search(r'(https?://[^\s]+|ewell\.se|mfwebblearning\.se|ehelper\.se|paleoreceptboken\.se|veggieswap\.com|pplanner\.se|pplannermini\.se|dandyville\.se|shapy\.se|pounced\.com\.au|eyeeco\.com|gangaji\.org|hubcrm\.com\.au|sugar\.snappromotions\.com|upsac\.org|winehunter\.com|djmserver\.com/music|oxfordandbeamount\.com|choirshowcase\.com/vote|phase3productions\.com|bfmt\.com\.br|exactmining\.com\.au|CAMIS|Sales Force Automation|Visualize System|Estimation Generation System|Finance Management System|Variable Operating Cost System)', chunk)
        
        name = "Unknown Project"
        link = "#"
        if url_match:
            raw_name = url_match.group(0)
            if raw_name.startswith('http'):
                link = raw_name
                name = raw_name.replace('https://', '').replace('http://', '').replace('www.', '').strip('/')
            else:
                # Assume it's a domain if it has a dot, otherwise just a name
                if '.' in raw_name and ' ' not in raw_name:
                    link = 'https://' + raw_name
                    name = raw_name
                else:
                    link = "#"
                    name = raw_name
        
        # Extract Company
        companies = ["IndiaNIC Infotech Ltd", "IndaPoint Tech. Pvt. Ltd.", "Biztech Consultancy", "Infosoft", "CMC Ltd.", "IPCL"]
        company = "Unknown Company"
        for comp in companies:
            if comp in chunk:
                company = comp
                break
        
        # Extract Role
        roles = ["Lead Software Engineer", "Team Leader", "Developer", "Analyzer & Developer", "Project Trainee"]
        role = "Developer"
        for r in roles:
            if r in chunk:
                role = r
                break

        # Extract Environment/Tech Stack
        tech_keywords = ["Laravel", "PHP", "Go", "Python", "React", "JavaScript", "jQuery", "MySQL", "PostgreSQL", "MongoDB", "WordPress", "Svelte", "Filament", "NodeJs", "Angular", "Lumen", "Cake PHP", "Joomla", "SugarCRM", "Delphi7", "SQL Server", "JSP", "Servlet", "Oracle", "MS Access"]
        stack = []
        for tech in tech_keywords:
            if tech in chunk:
                stack.append(tech)
        
        # Extract Description
        desc_match = re.search(r'Description\s+(.*)', chunk, re.DOTALL)
        description = ""
        if desc_match:
            description = desc_match.group(1).strip()
            if "PERSONAL PROFILE" in description:
                description = description.split("PERSONAL PROFILE")[0]
        
        projects.append({
            "name": name,
            "link": link,
            "company": company,
            "role": role,
            "stack": stack,
            "description": description
        })
        
    return projects


# Manual configuration
MANUAL_LOGOS = {
    "onlymaldives.com": "https://www.onlymaldives.com/wp-content/uploads/2025/09/project-logo.webp",
    "vibe.kmbs.co.in": "https://vibe.kmbs.co.in/images/admin/vibe-logo.svg",
    "tashbyt.com": "https://www.tashbyt.com/assets/images/logo.svg",
    "robotshutters.com": "https://www.robotshutters.com/images/logo.jpg",
    "eyeeco.com": "https://prnvision.com/cdn/shop/files/ee-logo-header-270x52.svg?height=90&v=1750425668",
    "gangaji.org": "https://gangaji.org/wp-content/uploads/2022/10/gangaji_logo-new.png"
}

FORCE_LINK = ["maxxsports.tv"]
FORCE_UNLINK = ["theweedtube.com"]

def verify_and_fetch_logo(project):
    link = project['link']
    name = project['name']
    
    # Check for forced unlink
    if any(u in link or u in name for u in FORCE_UNLINK):
        return False, None

    # Check for forced link status (we still verify if it's reachable unless we just trust it)
    # The user said "add link", implying it might have been failed by the check.
    # We will treat it as working if in FORCE_LINK.
    is_forced_working = any(u in link or u in name for u in FORCE_LINK)
    
    if link == "#" and not is_forced_working:
        return False, None

    print(f"Checking {link}...")
    
    is_working = False
    if is_forced_working:
        is_working = True
        print(f"  Forced working for {link}")
    else:
        # 1. Verify URL
        try:
            req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.getcode() == 200:
                    is_working = True
        except Exception as e:
            print(f"  Failed to reach {link}: {e}")
            is_working = False

    # 2. Fetch Logo
    logo_path = None
    
    # Check manual logos first
    manual_logo_url = None
    for key, url in MANUAL_LOGOS.items():
        if key in link or key in name:
            manual_logo_url = url
            break
            
    if manual_logo_url:
        try:
            ext = manual_logo_url.split('.')[-1].split('?')[0]
            if len(ext) > 4: ext = "jpg" # fallback
            
            domain = name # use name as filename base
            save_path = f"images/projects/{domain}.{ext}"
            
            # Download with user agent
            req = urllib.request.Request(manual_logo_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(save_path, 'wb') as out_file:
                out_file.write(response.read())
                
            logo_path = save_path
            print(f"  Saved manual logo to {save_path}")
        except Exception as e:
            print(f"  Error fetching manual logo from {manual_logo_url}: {e}")

    # If no manual logo, try clearbit (only if we didn't just fail a manual attempt, 
    # but actually we can fallback if manual fails? Let's just stick to manual if defined)
    if not logo_path and not manual_logo_url and link != "#":
        try:
            domain = urlparse(link).netloc
            if not domain:
                domain = link 
            
            domain = domain.replace('www.', '')
            
            logo_url = f"https://logo.clearbit.com/{domain}"
            save_path = f"images/projects/{domain}.png"
            
            # Check if already exists to avoid re-downloading everything every time? 
            # For now, just overwrite or try download.
            try:
                urllib.request.urlretrieve(logo_url, save_path)
                logo_path = save_path
                print(f"  Saved logo to {save_path}")
            except Exception as e:
                print(f"  No logo found for {domain}")
                
        except Exception as e:
            print(f"  Error fetching logo: {e}")

    return is_working, logo_path


def generate_html(projects):
    html = """
        <!-- Projects Section -->
        <section class="section" id="projects">
            <div class="section-content">
                <h2 class="section-title">
                    <span class="title-number">05.</span>
                    Projects
                </h2>
                <div class="projects-grid">
    """
    
    for p in projects:
        # Skip the "Unknown Project" if it slipped in
        if p['name'] == "Unknown Project" and len(p['description']) < 10:
            continue

        is_working, logo_path = verify_and_fetch_logo(p)
        
        stack_html = ""
        for tech in p['stack']:
            stack_html += f'<span class="project-tech-tag">{tech}</span>\n'
            
        # Image HTML
        if logo_path:
            image_html = f'<div class="project-logo"><img src="{logo_path}" alt="{p["name"]} logo"></div>'
        else:
            # Placeholder image
            image_html = f'<div class="project-logo"><img src="images/projects/placeholder.png" alt="Project placeholder"></div>'

        # Title HTML
        if is_working:
            title_html = f'<a href="{p["link"]}" target="_blank" class="project-title">{p["name"]} <i class="fas fa-external-link-alt text-xs ml-1"></i></a>'
        else:
            title_html = f'<span class="project-title">{p["name"]}</span>'
            
        html += f"""
                    <div class="card project-card">
                        <div class="project-header-row">
                            {image_html}
                            <div class="project-header-info">
                                {title_html}
                                <div class="project-company">{p['company']}</div>
                            </div>
                        </div>
                        <div class="project-role">{p['role']}</div>
                        <div class="project-description">
                            {p['description']}
                        </div>
                        <div class="project-tech-stack">
                            {stack_html}
                        </div>
                    </div>
        """
        
    html += """
                </div>
            </div>
        </section>
    """
    return html

print("Parsing projects...")
projects = parse_projects('temp_cv.txt')
print(f"Found {len(projects)} projects.")

print("Generating HTML...")
html_content = generate_html(projects)

with open('projects_section_v2.html', 'w') as f:
    f.write(html_content)

print("HTML generated in projects_section_v2.html")
