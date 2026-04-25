# 🤖 AWS Bedrock Chatbot

A Python-based AI chatbot application powered by **Amazon Bedrock**, featuring separate **Admin** and **User** interfaces with Docker support.

---

## 📋 Overview

This project leverages Amazon Bedrock's foundation models to build an intelligent chatbot with:
- **Admin panel** — manage configurations, knowledge bases, and model settings
- **User interface** — interact with the AI chatbot powered by AWS Bedrock
- **Dockerized deployment** — easy setup and consistent environments

---

## 🏗️ Project Structure

```
aws-bedrock-chatbot/
├── Admin/              # Admin panel - configuration & management
├── User/               # User-facing chatbot interface
├── Dockerfile          # Docker container configuration
└── README.md
```

---

## 🚀 Features

- 💬 Conversational AI powered by **Amazon Bedrock** foundation models
- 📄 **Chat with PDF** — upload documents and ask questions (RAG)
- 🔐 Separate **Admin** and **User** roles
- 🐳 **Docker** support for easy deployment
- ☁️ Fully serverless, AWS-native architecture

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application language |
| Amazon Bedrock | Foundation model API (Claude, Titan, etc.) |
| Amazon S3 | Document storage for RAG |
| Amazon OpenSearch | Vector store for embeddings |
| Docker | Containerized deployment |

---

## ⚙️ Prerequisites

- Python 3.10+
- AWS Account with Bedrock access enabled
- AWS CLI configured (`aws configure`)
- Docker (optional, for containerized run)
- IAM permissions for Bedrock, S3, and OpenSearch

---

## 🔧 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/github-surendra/aws-bedrock-chatbot.git
cd aws-bedrock-chatbot
git checkout develop
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure AWS Credentials
```bash
aws configure
```
Or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### 5. Set Environment Variables
```bash
cp .env.example .env
```
Edit `.env`:
```
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
S3_BUCKET_NAME=your-bucket-name
```

---

## ▶️ Running the Application

### Local Run

**Admin Panel:**
```bash
cd Admin
python app.py
```

**User Interface:**
```bash
cd User
python app.py
```

### Docker Run
```bash
# Build image
docker build -t aws-bedrock-chatbot .

# Run container
docker run -p 8080:8080 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_DEFAULT_REGION=us-east-1 \
  aws-bedrock-chatbot
```

---

## 🧠 How It Works (RAG Architecture)

```
User Query
    │
    ▼
Embed Query (Bedrock Embedding Model)
    │
    ▼
Semantic Search (OpenSearch Vector Store)
    │
    ▼
Retrieve Relevant Documents (Context)
    │
    ▼
Augmented Prompt = Query + Context
    │
    ▼
Amazon Bedrock Foundation Model
    │
    ▼
AI Response
```

---

## 🔐 IAM Permissions Required

Attach the following policies to your IAM user/role:

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeModel",
    "bedrock:InvokeModelWithResponseStream",
    "bedrock-agent:*",
    "s3:GetObject",
    "s3:PutObject",
    "s3:ListBucket"
  ],
  "Resource": "*"
}
```

---

## 🌿 Branching Strategy

| Branch | Purpose |
|---|---|
| `main` | Production-ready code |
| `develop` | Active development |
| `feature/*` | New features |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request to `develop`

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Surendra Shrestha**
- GitHub: [@github-surendra](https://github.com/github-surendra)

---

> Built with ❤️ using Amazon Bedrock and Python
