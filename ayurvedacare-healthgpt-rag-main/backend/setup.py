from setuptools import setup, find_packages

setup(
    name="healthgpt-backend",
    version="1.0.0",
    description="HealthGPT Backend - RAG-based Health Assistant",
    packages=find_packages(),
    install_requires=[
        'flask==2.3.3',
        'flask-cors==4.0.0',
        'python-dotenv==1.0.0',
        'groq==0.4.1',
        'chromadb==0.4.15',
        'ollama==0.1.7',
        'PyPDF2==3.0.1',
        'python-docx==0.8.11',
        'sentence-transformers==2.2.2',
        'numpy==1.24.3',
        'requests==2.31.0',
    ],
    python_requires='>=3.10',
    author="HealthGPT Team",
    author_email="team@healthgpt.com",
)
