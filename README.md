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

### Project Structure
1. **UPLOAD_FOLDER** : All the files (pdf, word or text) that will be uploaded will get stored here. It contains two files as samples.
2. **src** : It contains the **exception.py** file for handling Custom Exceptions and the **logger.py** file which creates log files that helps us track our progress while the project is running and also stores the exceptions occured. The **utils.py** file contains two classes : the first to handle summarizing using LED Model and the second to generate tokens and embedding vectors of text using Huggingface BERT model.
3. **src.components**: The src folder has a subfolder names components, which stores two files : **data_transformation.py** which can separate out the text from pdf, text or word files as paragraphs and the **web_scraping.py** file which can extract the headers and paragraphs from websites.
4. **Templates:** The templates folder contains the **HTML code** for our frontend page.
5. The **app.py** is a Flask app that provides endpoints to the webapp to perform the different tasks : uploading of documents, taking url , keywords , number of characters as inputs, display summaries and extracted texts, etc.
6. The **requirements.txt** file contains all the Python modules required in the project.

### Snapshot of the project
![image](https://github.com/Attention-is-All-We-Need/Document-Summary-Generator/assets/95437455/abb2019c-deb4-4e21-b400-c8a81fb1301c)
It can summarize Webpages, and PDF Files including research articles, for you!

# The team members are :
1. Anwesh Saha (https://github.com/Anweshbyte)
2. Arindom Bora (https://github.com/AriBora)
3. Ajay Sankar Makkena (https://github.com/mas622424)
4. Khush Khandelwal (https://github.com/khandelwalkhush05)
5. Vineet Kumar (https://github.com/Vineet-the-git)
6. Shreyash Nallawar (https://github.com/NShreyash)
