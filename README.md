<div align="center">
  <a href="https://soligit.com">
    <img src="public/favicon.ico" alt="Soligit Logo" width="100" height="100">
  </a>
  <h1 align="center">Soligit</h1>
  <p align="center">
    <strong>Streamline Your Development Workflow with AI</strong>
  </p>
  <p align="center">
    Soligit is a powerful open-source tool that leverages AI to automatically generate comprehensive documentation for your codebases, analyze and summarize meetings, and provide intelligent insights into your projects.
  </p>
  <p align="center">
    <a href="/LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
    <a href="https://github.com/your-username/soligit/issues"><img src="https://img.shields.io/github/issues/your-username/soligit" alt="Issues"></a>
    <a href="https://github.com/your-username/soligit/stargazers"><img src="https://img.shields.io/github/stars/your-username/soligit" alt="Stargazers"></a>
  </p>
</div>

## ✨ Features

- **🤖 Automated Documentation Generation:** Provide a GitHub URL and receive a full-fledged documentation website, complete with a file tree and answers to common questions about your codebase.
- **🧠 AI-Powered Q&A:** Ask questions about your codebase in natural language and get intelligent, context-aware answers.
- **⏱️ Commit Summarization:** Automatically summarize the changes in a specific commit, making it easier to track project history.
- **🎙️ Meeting Transcription and Analysis:** Transcribe audio meetings from a URL and use AI to summarize key points and answer questions about the discussion.
- **🔒 Secure and Scalable:** Built with a modern, robust tech stack to ensure reliability and performance.

## 🚀 Tech Stack

### Frontend

| Technology | Icon |
| --- | --- |
| Next.js | <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js"> |
| React | <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React"> |
| TypeScript | <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript"> |
| Tailwind CSS | <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS"> |
| tRPC | <img src="https://img.shields.io/badge/tRPC-2596BE?style=for-the-badge&logo=trpc&logoColor=white" alt="tRPC"> |
| shadcn/ui | <img src="https://img.shields.io/badge/shadcn/ui-000000?style=for-the-badge&logo=shadcn&logoColor=white" alt="shadcn/ui"> |
| Clerk | <img src="https://img.shields.io/badge/Clerk-6C47FF?style=for-the-badge&logo=clerk&logoColor=white" alt="Clerk"> |

### Backend

| Technology | Icon |
| --- | --- |
| Python | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"> |
| FastAPI | <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"> |
| Weaviate | <img src="https://img.shields.io/badge/Weaviate-101523?style=for-the-badge&logo=weaviate&logoColor=white" alt="Weaviate"> |
| Google Gemini | <img src="https://img.shields.io/badge/Google_Gemini-8E44AD?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Google Gemini"> |
| AssemblyAI | <img src="https://img.shields.io/badge/AssemblyAI-FFB300?style=for-the-badge&logo=assemblyai&logoColor=white" alt="AssemblyAI"> |

## 🏗️ Production-Grade Infrastructure

Soligit is designed for robust, scalable, and secure deployments. Our recommended production setup uses **Azure Cloud** with:

- Automated VM provisioning using **Terraform**
- Secure networking (NSG firewall rules)
- Nginx reverse proxy for HTTPS and load balancing
- Supervisor for backend process management
- Automated deployment scripts
- Environment variable management for secrets
- Logging and monitoring best practices

See [`infrastructure/azure/README.md`](infrastructure/azure/README.md) for full instructions and architecture details.

### Key Features
- **Scalable VM** with Ubuntu 22.04
- **Nginx** reverse proxy for production
- **Supervisor** for process management
- **Auto-deployment** from GitHub
- **Firewall** (SSH, HTTP, HTTPS, FastAPI)
- **Cost-effective** (~$35-50/month)
- **Security best practices** (no secrets in git, HTTPS, regular updates)

---

### Prerequisites

- Node.js (v18 or later)
- Python (v3.9 or later)
- `pip` and `virtualenv` for Python package management
- A PostgreSQL database

## 🛠️ Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/soligit.git
    cd soligit
    ```

2.  **Set up the frontend:**
    ```bash
    npm install
    ```

3.  **Set up the backend:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    cd ..
    ```

4.  **Set up environment variables:**
    Create a `.env.local` file in the root directory and add the following, replacing the placeholder values with your actual credentials:
    ```env
    # Clerk Authentication
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
    CLERK_SECRET_KEY=your_clerk_secret_key

    # Database
    DATABASE_URL="postgresql://user:password@host:port/database"

    # Weaviate
    WEAVIATE_ENVIRONMENT=your_weaviate_environment
    WEAVIATE_API_KEY=your_weaviate_api_key
    WEAVIATE_INDEX=your_weaviate_index

    # GitHub
    GITHUB_PERSONAL_ACCESS_TOKEN=your_github_personal_access_token
    ```

5.  **Run database migrations:**
    ```bash
    npm run db:migrate
    ```

### Running the Application

1.  **Start the backend server:**
    ```bash
    cd backend
    uvicorn main:app --reload
    ```

2.  **Start the frontend development server:**
    In a separate terminal, from the root directory:
    ```bash
    npm run dev
    ```

Your application should now be running at `http://localhost:3000`.

## 📂 Project Structure

### Infrastructure

```
infrastructure/
  azure/           # Terraform files for Azure VM, networking, security, cloud-init
  scripts/         # Bash scripts for deployment and destruction
```

See [`infrastructure/azure/README.md`](infrastructure/azure/README.md) for full cloud deployment instructions.

```
soligit/
├── backend/         # Python FastAPI backend
├── prisma/          # Prisma schema and migrations
├── public/          # Public assets
├── src/             # Next.js frontend application
│   ├── app/         # App Router pages and layouts
│   ├── components/  # React components
│   ├── lib/         # Helper functions and utilities
│   ├── server/      # Server-side logic (tRPC, db)
│   └── trpc/        # tRPC configuration
├── .env.local       # Environment variables (create this)
├── package.json     # Frontend dependencies and scripts
└── README.md        # This file
```

## 🏆 Quality & Security

- **Infrastructure as Code:** All cloud resources are managed via Terraform for reproducibility and auditability.
- **Secrets Management:** `.env` files are never committed; sensitive data is managed securely.
- **Automated Deployment:** VM setup and app deployment are fully automated for reliability.
- **Logging & Monitoring:** Nginx and Supervisor logs are available for troubleshooting and monitoring.
- **Cost & Performance:** Default VM size is cost-effective for most use cases; easily upgradable.
- **Security:** NSG rules, HTTPS, and regular updates recommended.

## 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the **Apache 2.0 License**. See the [LICENSE](LICENSE) file for details.

## 🔒 Security

For production deployment, see [`infrastructure/azure/README.md`](infrastructure/azure/README.md) for security best practices, cost estimation, and troubleshooting tips.

For any security-related concerns, please refer to our [Security Policy](SECURITY.md).