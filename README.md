# OWASPGPT-10
The goal of OWASP-GPT10 is to assist teams in crafting more thorough threat models using OWASP top 10 methadology. It achieves this by harnessing the capabilities of OpenAI's GPT models to generate lists of threats and mitigations

# Installation

Option 1: Cloning the Repository

Clone this repository:

```
git clone git@github.com:san3ncrypt3d/OWASPGPT-10.git

```
Change to the cloned repository directory:

```
cd OWASPGPT-10

```
Install the required Python packages:

```
pip install -r requirements.txt

```

Run the Streamlit app:

```
streamlit run function.py

```
Open the app in your web browser using the provided URL.



# Using Docker Container

Run the Docker container:

```
docker build -t OWASPGPT-10 .

```

```
docker run -p 8501:8501 OWASPGPT-10

```

Open a web browser and navigate to http://localhost:8501 to access the app running inside the container.




# Option : Using Docker Container

Pull the Docker image from Docker Hub:

```
docker pull

```
