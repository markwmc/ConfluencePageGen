import os
import base64
import requests
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request


load_dotenv()

CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

app = Flask(__name__)

def create_page(space_id, title, parent_id=None):
    auth_string = f"{CONFLUENCE_EMAIL}:{CONFLUENCE_API_TOKEN}"
    base64_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

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
                <p>This is where the main content of the {title} will go. </p>
                <h3 id="section1">Section 1</h3>
                <p>Details about section 1...</p>
                <h3 id="section2">Section 2</h3>
                <p>Details about section 2..</p>
            </ac:layout-cell>

            <ac:layout-cell>
                <!-- Right Sidebar Content: Table of Contents -->
                <h3>On This Page</h3>
                <ac:macro ac:name="toc">
                    <ac:parameter ac:name="Style">square</ac:parameter>
                    <ac:parameter ac:name="maxLevel">3</ac:parameter>
                    <ac:parameter ac:name="minLevel">2</ac:parameter>
                </ac:macro>
            </ac:layout-cell>
        </ac:layout-section>
    </ac:layout>

    <h2>Additional Information</h2>
    <p<Additional content or instructions can go here.</p>
    """

    data = {
        "type": "page",
        "title": title,
        "space": {"key": space_id},
        "body": {
            "storage":{
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

    print(f"Attempting to create page: {title}"
    response = requests.post(
        CONFLUENCE_BASE_URL + "/content",
        headers=headers,
        json=data,
    )
    
    if response)
