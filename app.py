import requests
import base64
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Confluence API URL (for cloud)
CONFLUENCE_API_URL = os.getenv('CONFLUENCE_BASE_URL')

# Retrieve the email and API token from environment variables
CONFLUENCE_EMAIL = os.getenv('CONFLUENCE_EMAIL')
CONFLUENCE_API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN')

app = Flask(__name__)

def create_page(space_id, title, parent_id=None):
    # Create the basic auth header using email and API token
    auth_string = f"{CONFLUENCE_EMAIL}:{CONFLUENCE_API_TOKEN}"
    base64_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    # Define the page content with formatting: 2-column layout, table of contents on the right
    content = f"""
    <h1>{title}</h1>
    <p>This is the {title} section.</p>

    <!-- Excerpt block -->
    <ac:macro ac:name="excerpt">
        <ac:parameter ac:name="name">page-focus</ac:parameter>
        <ac:rich-text-body>
            <p>{title} content preview</p>
        </ac:rich-text-body>
    </ac:macro>

    <!-- Set the page layout to 2 columns -->
    <ac:layout>
        <ac:layout-section ac:type="two_equal">
            <ac:layout-cell>
                <!-- Left Sidebar Content -->
                <h2>Content</h2>
                <p>This is where the main content of the {title} will go.</p>
                <h3 id="section1">Section 1</h3>
                <p>Details about section 1...</p>
                <h3 id="section2">Section 2</h3>
                <p>Details about section 2...</p>
            </ac:layout-cell>

            <ac:layout-cell>
                <!-- Right Sidebar Content: Table of Contents -->
                <h3>On This Page</h3>
                <ac:macro ac:name="toc">
                    <ac:parameter ac:name="style">square</ac:parameter>
                    <ac:parameter ac:name="maxLevel">3</ac:parameter>
                    <ac:parameter ac:name="minLevel">2</ac:parameter>
                </ac:macro>
            </ac:layout-cell>
        </ac:layout-section>
    </ac:layout>

    <h2>Additional Information</h2>
    <p>Additional content or instructions can go here.</p>
    """

   
    data = {
        "type": "page",
        "title": title,
        "space": {"key": space_id},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }

    if parent_id:
        data["ancestors"] = [{"id": parent_id}]

    headers = {
        "Authorization": f"Basic {base64_auth}",
        "Content-Type": "application/json"
    }

    print(f"Attempting to create page: {title}")
    response = requests.post(
        CONFLUENCE_API_URL + "/content",
        headers=headers,
        json=data,
    )

    if response.status_code == 200:
        print(f"✅ Page '{title}' created successfully!")
        return response.json()
    else:
        print(f"❌ Failed to create page: {title}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    success = False
    if request.method == "POST":
        space_id = request.form.get("space_id")

        
        titles = {
            "User Guide": "📚 User Guide",  
            "Design & Architecture": "📐 Design & Architecture",
            "Product Development": "💡 Product Development",  
            "Administration": "⚙️ Administration",
            "Help & Support": "🛟 Help & Support"
        }

        # Step 1: Create User Guide page
        user_guide_title = titles["User Guide"]
        user_guide_page_response = create_page(space_id, user_guide_title)
        if user_guide_page_response:
            user_guide_page_id = user_guide_page_response['id']
            print(f"User Guide page created successfully! ID: {user_guide_page_id}")

            # Step 2: Create child pages under the User Guide page
            child_pages = [
                "List of Features",
                "How To Page",
                "Feature Walkthroughs"
            ]
            for child_page in child_pages:
                child_page_response = create_page(space_id, child_page, parent_id=user_guide_page_id)
                if child_page_response:
                    print(f"Child Page '{child_page}' created successfully!")
                    success = True
                else:
                    print(f"Failed to create child page: {child_page}")
        else:
            print(f"Failed to create User Guide page")

        # Step 3: Create the top-level pages (Design & Architecture, Product Development, Administration, Help & Support)
        design_architecture_page_id = None
        product_development_page_id = None
        administration_page_id = None
        help_and_support_page_id = None
        top_level_pages = [
            ("Design & Architecture", titles["Design & Architecture"]),
            ("Product Development", titles["Product Development"]),  # New page between Design & Architecture and Administration
            ("Administration", titles["Administration"]),
            ("Help & Support", titles["Help & Support"])
        ]
        
        for page_name, title in top_level_pages:
            page_response = create_page(space_id, title)
            if page_response:
                print(f"Top-Level Page '{title}' created successfully!")
                success = True
                if title == titles["Design & Architecture"]:
                    design_architecture_page_id = page_response['id']
                    print(f"Design & Architecture page created successfully! ID: {design_architecture_page_id}")
                elif title == titles["Product Development"]:
                    product_development_page_id = page_response['id']
                    print(f"Product Development page created successfully! ID: {product_development_page_id}")
                elif title == titles["Administration"]:
                    administration_page_id = page_response['id']
                    print(f"Administration page created successfully! ID: {administration_page_id}")
                elif title == titles["Help & Support"]:
                    help_and_support_page_id = page_response['id']
                    print(f"Help & Support page created successfully! ID: {help_and_support_page_id}")
            else:
                print(f"Failed to create top-level page: {page_name}")

        # Step 4: Add subpages for Design & Architecture
        if design_architecture_page_id:
            design_architecture_subpages = [
                "Design Overview",
                "Design Pages",
                "Future Feature Ideas"
            ]
            for subpage in design_architecture_subpages:
                subpage_response = create_page(space_id, subpage, parent_id=design_architecture_page_id)
                if subpage_response:
                    print(f"Subpage '{subpage}' created successfully!")
                    success = True
                else:
                    print(f"Failed to create subpage: {subpage}")

        # Step 5: Add subpages for Product Development
        if product_development_page_id:
            product_development_subpages = [
                "Development Overview Section",
                "Requirements Section",
                "Development Environment Setup",
                "Workstation Requirements",
                "Programming Languages",
                "Frameworks or Packages",
                "GitHub Repo(s) Links",
                "Release Notes",
                "Certifications (devices, browsers, etc)",
                "CI/CD Process",
                "Quality Assurance",
                "Automation Testing",
                "Manual Testing"
            ]
            for subpage in product_development_subpages:
                subpage_response = create_page(space_id, subpage, parent_id=product_development_page_id)
                if subpage_response:
                    print(f"Subpage '{subpage}' created successfully!")
                    success = True
                else:
                    print(f"Failed to create subpage: {subpage}")

        # Step 6: Add subpages for Administration
        if administration_page_id:
            administration_subpages = [
                "Deployments",
                "Installation Process",
                "Upgrade & Maintenance Process",
                "Health Checks / Smoke Tests",
                "Permissions",
                "System Logs",
                "Monitoring",
                "How To …"
            ]
            for subpage in administration_subpages:
                subpage_response = create_page(space_id, subpage, parent_id=administration_page_id)
                if subpage_response:
                    print(f"Subpage '{subpage}' created successfully!")
                    success = True
                else:
                    print(f"Failed to create subpage: {subpage}")

        # Step 7: Add subpages for Help & Support
        if help_and_support_page_id:
            help_and_support_subpages = [
                "Support Overview",
                "Links to Support Docs",
                "How To …",
                "FAQ",
                "Issue Tracking"
            ]
            for subpage in help_and_support_subpages:
                subpage_response = create_page(space_id, subpage, parent_id=help_and_support_page_id)
                if subpage_response:
                    print(f"Subpage '{subpage}' created successfully!")
                    success = True
                else:
                    print(f"Failed to create subpage: {subpage}")

    return render_template('index.html', success=success)

if __name__ == '__main__':
    app.run(debug=True)
