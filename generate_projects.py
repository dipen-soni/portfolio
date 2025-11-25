import re

def parse_projects(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Split by "Project" keyword which seems to start each project block in the text
    # The text extraction might be a bit messy, so we need to be careful.
    # Looking at the text, it seems to follow a pattern:
    # Project Company Name Environment Database Role
    # <Link> <Company> <Env> <DB> <Role>
    # Description
    # <Description text>

    # Let's try to find blocks starting with "Project" and capture the fields.
    # Since the text is just a long string with some structure, regex might be best.
    
    # We can split by "Project" and then process each chunk.
    chunks = content.split("Project")
    
    projects = []
    
    # Skip the first chunk as it's the header/intro
    for chunk in chunks[1:]:
        # Clean up the chunk
        chunk = chunk.strip()
        
        # It seems the fields are somewhat sequential.
        # Let's try to extract the link (Project Name), Company, Environment, Database, Role, Description
        
        # Extract Link/Name
        # It seems to be the first thing after "Company Name Environment Database Role" header lines which might be mixed in.
        # Actually, the text "Company Name Environment Database Role" appears at the start of the chunk usually.
        
        # Let's try to find the URL.
        url_match = re.search(r'(https?://[^\s]+|ewell\.se|mfwebblearning\.se|ehelper\.se|paleoreceptboken\.se|veggieswap\.com|pplanner\.se|pplannermini\.se|dandyville\.se|shapy\.se|pounced\.com\.au|eyeeco\.com|gangaji\.org|hubcrm\.com\.au|sugar\.snappromotions\.com|upsac\.org|winehunter\.com|djmserver\.com/music|oxfordandbeamount\.com|choirshowcase\.com/vote|phase3productions\.com|bfmt\.com\.br|exactmining\.com\.au|CAMIS|Sales Force Automation|Visualize System|Estimation Generation System|Finance Management System|Variable Operating Cost System)', chunk)
        
        name = "Unknown Project"
        link = "#"
        if url_match:
            name = url_match.group(0)
            link = name if name.startswith('http') else '#'
            # Clean up name if it's a URL
            if name.startswith('http'):
                name = name.replace('https://', '').replace('http://', '').replace('www.', '').strip('/')
        
        # Extract Company
        # Company seems to be after the link/name.
        # This is tricky with just text. Let's look for known companies.
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
        # We can look for keywords.
        tech_keywords = ["Laravel", "PHP", "Go", "Python", "React", "JavaScript", "jQuery", "MySQL", "PostgreSQL", "MongoDB", "WordPress", "Svelte", "Filament", "NodeJs", "Angular", "Lumen", "Cake PHP", "Joomla", "SugarCRM", "Delphi7", "SQL Server", "JSP", "Servlet", "Oracle", "MS Access"]
        stack = []
        for tech in tech_keywords:
            if tech in chunk:
                stack.append(tech)
        
        # Extract Description
        # Description seems to start after "Description" keyword.
        desc_match = re.search(r'Description\s+(.*)', chunk, re.DOTALL)
        description = ""
        if desc_match:
            description = desc_match.group(1).strip()
            # Truncate if it goes into the next project or section (though we split by Project already)
            # But the last project might have extra text.
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
        stack_html = ""
        for tech in p['stack']:
            stack_html += f'<span class="project-tech-tag">{tech}</span>\n'
            
        link_html = f'<a href="{p["link"]}" target="_blank" class="project-title">{p["name"]}</a>' if p["link"] != "#" else f'<span class="project-title">{p["name"]}</span>'
            
        html += f"""
                    <div class="card project-card">
                        <div class="project-header">
                            {link_html}
                        </div>
                        <div class="project-company">{p['company']}</div>
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

projects = parse_projects('temp_cv.txt')
html_content = generate_html(projects)

with open('projects_section.html', 'w') as f:
    f.write(html_content)

print("HTML generated in projects_section.html")
