# All in one Jenkins based Dynamic Application Security Testing Pipeline:
This Jenkins pipeline script defines a complete security testing and report generation workflow with multiple stages and parameters. Here is a summary and some key points of the pipeline:

# Parameters:
The pipeline allows users to choose the attack tool (ATTACK_TOOL_TYPE), scan type (SCAN_TYPE), target URL(s) (NEED_TO_SCAN_VARIABLE), and other options like API type and email settings for report generation.

# Stages:-

# Pipeline Info: 
Outputs the current parameters for the scan.

# Python-Scripts-Download: 
Downloads necessary Python scripts for the scan.

# Need-to-Scan-URL(s): 
Processes the URLs that need to be scanned, either based on predefined subdomains or user input.

# Setting-up-environment: 
Sets up Docker containers for OWASP ZAP or other tools like Nikto, SQLMap, and Nmap depending on the selected tool.

# Prepare-Working-directory: 
Prepares the working directory for generating reports.

# Penetration-Testing-Process: 
Executes the chosen tool based on the scan type. This includes OWASP ZAP, Nikto, SQLMap, Nmap, etc. For each tool, it scans URLs and stores the number of alerts generated.

# Copying-Report-to-Workspace: 
Copies the scan reports from the container to the workspace.

# Report-Uploading-To-Nexus: 
Uploads the reports to a Nexus repository.

# Report-Email-Sending: 
Sends the generated report to a specified email address using a custom SMTP Python script.

# Post Actions:
1. The pipeline includes cleanup steps (always, failure, success) that ensure the Docker container is removed and the workspace is cleaned.
2. It has status reporting for success, failure, unstable, and changed pipeline states.

# Key Enhancements/Notes:
1. The pipeline integrates Docker containers for running security tools.
2. There is flexibility for scanning based on user-defined parameters.
3. Reports are handled and uploaded automatically, and there is a mechanism for emailing the results.
