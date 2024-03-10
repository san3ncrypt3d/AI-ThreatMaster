import json
import streamlit as st
import streamlit.components.v1 as components
import re
from openai import OpenAI
from openai import AzureOpenAI


def get_input():
    input_text = st.text_area(
        label="Describe the scenario for generating threats among with details of the application (eg. front-end: Angular , backend: Flask)",
        placeholder="Enter the details.....",
        height=150,
        key="T_Input",
        help="Enter in-depth overview of the application, covering its intended use, the technologies employed, and any pertinent details, or enter situation for which you need threats for. eg: An innovative fitness hub powered by React and Node.js. Crafted workout plans, exercise tracking, and live feedback for personalized fitness. Engage with a vibrant community—share achievements and tips. application support log in, register, forgot password etc. The app use OAuth2, MFA.",
    )
    return input_text


def create_tm_prmpt(T_App, T_Auth, T_facing, T_Clsfcn, pam, T_Input):
    prompt = f"""
Act as a cyber security specilist with more than 30 years experience, you are using the OWASP Top 10 for web, mobile, cloud, Desktop, api and IOT as threat modelling methodology to produce comprehensive threat models for a wide range of applications. Your task is to use the application description provided to you to produce a list of specific threats for the application, create all the possible threats atleast 10. Your analysis should provide a credible scenario in which each threat could occur in the context of the application. It is very important that your responses are tailored to reflect the details you are given.

Here is the Mapping for each OWASP TOP 10 Methadology: "
OWASP WEB TOP 10
A01:2021-Broken Access Control
A02:2021-Cryptographic Failures
A03:2021-Injection 
A04:2021-Insecure Design
A05:2021-Security Misconfiguration 
A06:2021-Vulnerable and Outdated Components
A07:2021-Identification and Authentication Failures 
A08:2021-Software and Data Integrity Failures 
A09:2021-Security Logging and Monitoring Failures 
A10:2021-Server-Side Request Forgery

OWASP MOBILE TOP 10

M1: Improper Credential Usage
M2: Inadequate Supply Chain Security
M3: Insecure Authentication/Authorization
M4: Insufficient Input/Output Validation
M5: Insecure Communication
M6: Inadequate Privacy Controls
M7: Insufficient Binary Protections
M8: Security Misconfiguration
M9: Insecure Data Storage
M10: Insufficient Cryptography

OWASP DESKTOP TOP 10

DA1 - Injections
DA2 - Broken Authentication & Session Management
DA3 - Sensitive Data Exposure	
DA4 - Improper Cryptography Usage
DA5 - Improper Authorization	
DA6 - Security Misconfiguration	
DA7 - Insecure Communication	
DA8 - Poor Code Quality	
DA9 - Using Components with Known Vulnerabilities	
DA10 - Insufficient Logging & Monitoring	


OWASP CLOUD TOP 10

CNAS-1: Insecure cloud, container or orchestration configuration
CNAS-2: Injection flaws (app layer, cloud events, cloud services)
CNAS-3: Improper authentication & authorization
CNAS-4: CI/CD pipeline & software supply chain flaws
CNAS-5: Insecure secrets storage
CNAS-6: Over-permissive or insecure network policies
CNAS-7: Using components with known vulnerabilities
CNAS-8: Improper assets management
CNAS-9: Inadequate compute resource quota limits
CNAS-10: Ineffective logging & monitoring (e.g. runtime activity)

OWASP API TOP 10


API1:2023 - Broken Object Level Authorization
API2:2023 - Broken Authentication
API3:2023 - Broken Object Property Level Authorization
API4:2023 - Unrestricted Resource Consumption
API5:2023 - Broken Function Level Authorization
API6:2023 - Unrestricted Access to Sensitive Business Flows
API7:2023 - Server Side Request Forgery
API8:2023 - Security Misconfiguration
API9:2023 - Improper Inventory Management
API10:2023 - Unsafe Consumption of APIs


OWASP IOT TOP 10

I1 Weak, Guessable, or Hardcoded Passwords
I2 Insecure Network Services
I3 Insecure Ecosystem Interfaces
I4 Lack of Secure Update Mechanism
I5 Use of Insecure or Outdated Components
I6 Insufficient Privacy Protection
I7 Insecure Data Transfer and Storage
I8 Lack of Device Management
I9 Insecure Default Settings
I10 Lack of Physical Hardening
"

When providing the threat model, use a JSON formatted response with the keys "threat_model" and "improvement_suggestions". Under "threat_model", include an array of objects with the keys "Threat Category", "Scenario", "OWASP TOP 10 Methadology" and "Risk". 

Under "improvement_suggestions", include an array of strings with suggestions on how the threat modeller can improve their application description in order to allow the tool to produce a more comprehensive threat model.

APPLICATION TYPE: {T_App}
AUTHENTICATION TYPE: {T_Auth}
INTERNET FACING: {T_facing}
DATA CLASSIFICATION: {T_Clsfcn}
PRIVILEGED ACCESS MANAGEMENT: {pam}
APPLICATION DESCRIPTION: {T_Input}

Example of expected JSON response format:
  
    {{
      "threat_model": [
        {{
          "Threat Category": "Example Threat Category",
          "Scenario": "Example Scenario",
          "OWASP TOP 10 Methadology:" "Example OWASP TOP 10 Used",
          "Risk": "Example Risk"
        }}
        // ... more threats
      ],
      "improvement_suggestions": [
        "Example improvement suggestion.",
        // ... more suggestions
      ]
    }}
"""
    return prompt


def get_threat_model(api_key, model_name, prompt):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model_name,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    response_content = json.loads(response.choices[0].message.content)

    return response_content

def get_threat_model_azure(api_key, model_name, prompt):
    client = AzureOpenAI(
        azure_endpoint = azure_api_endpoint,
        api_key = azure_api_key,
        api_version = azure_api_version,
    )

    response = client.chat.completions.create(
        model = azure_deployment_name,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    response_content = json.loads(response.choices[0].message.content)

    return response_content

   
def json_to_markdown(threat_model, improvement_suggestions):
    markdown_output = "## Threat Model\n\n"
    
    markdown_output += "| Threat Category | Scenario | OWASP Top 10 Methadology | Risk |\n"
    markdown_output += "|-------------|----------|--------------|------------------|\n"
    
    for threat in threat_model:
        markdown_output += f"| {threat['Threat Category']} | {threat['Scenario']} | {threat['OWASP TOP 10 Methadology']} | {threat['Risk']} |\n"
    
    markdown_output += "\n\n## Improvement Suggestions\n\n"
    for suggestion in improvement_suggestions:
        markdown_output += f"- {suggestion}\n"
    
    return markdown_output


def remediation_prmpt(threats):
    prompt = f"""
Act as a cyber security expert with more than 20 years experience of using the OWASP Top 10 threat modelling methodology. Your task is to provide potential mitigations for the threats identified in the threat model. It is very important that your responses are tailored to reflect the details of the threats.

Your output should be in the form of a markdown table with the following columns:
    - Column A: Threat Category
    - Column B: Scenario
    - Column C: OWASP TOP 10 Methadology
    - Column D: Suggested Mitigation(s)

Below is the list of identified threats:
{threats}

YOUR RESPONSE (do not wrap in a code block):
"""
    return prompt


def remediation(api_key, model_name, prompt):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides threat mitigation strategies in Markdown format."},
            {"role": "user", "content": prompt}
        ]
    )

    mitigations = response.choices[0].message.content

    return mitigations


def remediation_azure(api_key, model_name, prompt):
    client = AzureOpenAI(
        azure_endpoint = azure_api_endpoint,
        api_key = azure_api_key,
        api_version = azure_api_version,
    )

    response = client.chat.completions.create(
        model = azure_deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides threat mitigation strategies in Markdown format."},
            {"role": "user", "content": prompt}
        ]
    )

    mitigations = response.choices[0].message.content

    return mitigations




st.set_page_config(
    page_title="AI-ThreatMaster",
    page_icon=":fire:",
    layout="wide",
    initial_sidebar_state="expanded",
)



col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("1.png", width=450)



T_Input = get_input()

col1, col2 = st.columns(2)

with col1:
    T_App = st.selectbox(
        label="Choose an application type",
        options=[
            "Web application",
            "API",
            "Mobile application",
            "Cloud application",
            "Desktop application",
            "IoT application",
            "N/A",
        ],
        key="T_App",
    )

    T_Clsfcn = st.selectbox(
        label="What is the data classification of the application?",
        options=[
            "Top Secret",
            "Restricted",
            "Confidential",
            "Internal",
            "Public",
            "N/A",
        ],
        key="T_Clsfcn",
    )

    pam = st.selectbox(
        label="Is the application using Privileged Account Management (eg. CyberArk )",
        options=["Yes", "No", "N/A"],
        key="pam",
    )


with col2:
    T_facing = st.selectbox(
        label="What is the exposure of the application (Internal Only/ Internet facing)",
        options=[
            "Internal",
            "Internet",
        ],
        key="T_facing",
    )

    T_Auth = st.multiselect(
        "What auth is enabled on the application?",
        ["Single Sign On", "MFA", "OAUTH2", "Basic", "Biometric T_Auth", "Certificate T_Auth"],
        key="T_Auth",
    )


st.sidebar.header("How to use AI-ThreatMaster")

with st.sidebar:
   
    use_azure = st.toggle('Use Azure OpenAI Service', key='use_azure')
    
    if use_azure:
        st.markdown(
        """
    1. Enter the Azure API key, endpoint and deployment name
    2. Enter the details of the application for the threat model (Technology stack, functionalities etc)
    3. Use the options such as "Generate Threat Model" or "Generate Mitigations"
    """
    )

        azure_api_key = st.text_input(
            "Azure OpenAI API key:",
            type="password",
            help="You can find your Azure OpenAI API key here: [Azure portal](https://portal.azure.com/).",
        )
        
        azure_api_endpoint = st.text_input(
            "Azure OpenAI endpoint:",
            help="Eg: https://YOUR_RESOURCE_NAME.openai.azure.com/",
        )

        azure_deployment_name = st.text_input(
            "Deployment name:",
        )
        
        st.info("Note: Use an 1106-preview model deployment.")

        azure_api_version = '2023-12-01-preview' # Update this as needed

        st.write(f"Azure API Version: {azure_api_version}")

    else:
        st.markdown(
        """
    1. Enter the API Key: [OpenAI API key](https://platform.openai.com/account/api-keys) 
    2. Select the GPT version & Provide details of the application 
    3. Use the options such as "Generate Threat Model" or "Generate Mitigations"
    """
    )
        
        openai_api_key = st.text_input(
            "Enter your OpenAI API key:",
            type="password",
            help="Find your OpenAI API key on the [OpenAI Website](https://platform.openai.com/account/api-keys).",
        )

        selected_model = st.selectbox(
            "Select the model you would like to use:",
            ["gpt-4-1106-preview", "gpt-3.5-turbo-1106"],
            key="selected_model",
            help="The 0613 models are updated and more steerable versions. See [this post](https://openai.com/blog/function-calling-and-other-api-updates) for more details.",
        )

    st.markdown("""---""")

st.sidebar.header("About")

with st.sidebar:
    st.markdown(
        "AI-ThreatMaster - [san3ncrypt3d](https://san3ncrypt3d.com)"
    )
    st.markdown(
        "The goal of AI-ThreatMaster is to assist teams in crafting more thorough threat models using OWASP top 10 methadology. It achieves this by harnessing the capabilities of OpenAI's GPT models to generate lists of threats and mitigations"
    )
    st.markdown("Created by [Sanjay Babu](https://www.linkedin.com/in/san3ncrypt3d/)")
    
    st.markdown("""---""")



st.sidebar.header("FAQs")

with st.sidebar:
    st.markdown(
        """
    ### **What is AI-ThreatMaster?**
    The OWASP (Open Web Application Security Project) Top 10 provides critical insights into the most prevalent security risks across various technology domains, including web applications, mobile apps, cloud services, APIs (Application Programming Interfaces), and the Internet of Things (IoT). These lists outline the most pressing vulnerabilities and threats within each domain, offering guidance and best practices to developers, security professionals, and organizations.
    """
    )
    st.markdown(
        """
    ### **How does AI-ThreatMaster work?**
    When you provide application description and other informations, the tool will use a GPT model to generate a threats for the application. The model uses the application description and details to generate a list of potential threats and then categorises each threat according to the OWASP Top 10 methodology.
    """
    )
    st.markdown(
        """
    ### **Where can I find OWASP Top 10**
    [OWASP Top 10 Web Application Risks](https://owasp.org/www-project-top-ten/),

    [OWASP Top 10 Mobile Application Risks](https://owasp.org/www-project-mobile-top-10/),

    [OWASP Top 10 Desktop Application Risks](https://owasp.org/www-project-desktop-app-security-top-10/),

    [OWASP Top 10 Cloud Risks](https://owasp.org/www-project-cloud-native-application-security-top-10/),

    [OWASP Top 10 API Risks](https://owasp.org/API-Security/editions/2023/en/0x11-t10/),

    [OWASP Top 10 IoT Risks](https://owasp.org/www-project-internet-of-things/).
    """
    )
   

st.markdown("""---""")



with st.expander("Threat Model", expanded=False):
    threat_model_submit_button = st.button(label="Generate Threat Model")

    if threat_model_submit_button and T_Input:
        threat_model_prompt = create_tm_prmpt(T_App, T_Auth, T_facing, T_Clsfcn, pam, T_Input)

        with st.spinner("....Creating threats..."):
            try:
                if use_azure:
                    model_output = get_threat_model_azure(azure_api_key, azure_deployment_name, threat_model_prompt)
                else:
                    model_output = get_threat_model(openai_api_key, selected_model, threat_model_prompt)
                        
                threat_model = model_output.get("threat_model", [])
                improvement_suggestions = model_output.get("improvement_suggestions", [])

                st.session_state['threat_model'] = threat_model

                markdown_output = json_to_markdown(threat_model, improvement_suggestions)

                st.markdown(markdown_output)

            except Exception as e:
                st.error(f"Error: {e}")

            st.download_button(
                label="Download Threat Model",
                data=markdown_output, 
                file_name="AI-ThreatMaster_threat_model.md",
                mime="text/markdown",
            )

    if threat_model_submit_button and not T_Input:
        st.error("Try Again, After submitting application details.")




with st.expander("Mitigations", expanded=False):
    mitigations_submit_button = st.button(label="Generate Mitigations")

    if mitigations_submit_button:
        if 'threat_model' in st.session_state and st.session_state['threat_model']:
            threats_markdown = json_to_markdown(st.session_state['threat_model'], [])
            mitigations_prompt = remediation_prmpt(threats_markdown)

            with st.spinner("Looking for possible mitigations..."):
                try:
                    if use_azure:
                        mitigations_markdown = remediation_azure(azure_api_key, azure_deployment_name, mitigations_prompt)
                    else:
                        mitigations_markdown = remediation(openai_api_key, selected_model, mitigations_prompt)

                    st.markdown(mitigations_markdown)

                    st.download_button(
                        label="Download Mitigations",
                        data=mitigations_markdown,
                        file_name="mitigations.md",
                        mime="text/markdown",
                    )
                except Exception as e:
                    st.error(f"Error suggesting mitigations: {e}")
        else:
            st.error("Try Again.. After generating Threat(s).")
