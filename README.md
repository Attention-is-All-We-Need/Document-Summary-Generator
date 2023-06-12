# Document-Summary-Generator

**Document-Summary-Generator** is a repository for the Science and Technology Council Hackathon 2023, IIT Kanpur.
This repository contains our approach towards the problem statement **Generative AI for Impact**. We tried to implement a simple web page that can receive text from pdf,text,doc files, users or web pages and generate summary of the text using **Longformer Encoder-Decoder (LED)** model. The user can ask for different summary lengths. Moreover, we included a keyword search feature that enables users to ask questions about the text or generate summaries based on some keywords present in the text. The detailed documentation and user-guide can be found in the docs folder.

## Installation
### Requirements
1. Python 3.6 or higher
2. pip

### Setup Project
1. Fork the repository.
2. Clone the repository. In your terminal, type:
  <pre><code>git clone https://github.com/your-username/Document-Summary-Generator.git</code></pre>
3. Navigate to the repository directory : <code>cd Document-Summary-Generator</code>
4. Setup Python Virtual Environment : <code> virtualenv venv </code>
5. Activate the virtual environment. On Windows , <code>venv\Scripts\activate.bat</code>. On Linux/macOS , <code>source venv/bin/activate</code>.
5. Install the required modules : <code> pip install -r requirements.txt</code>
6. Run the **app.py** file and search http://127.0.0.1:8000 on the browser.
### Happy Coding!!!
