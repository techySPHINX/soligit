# Soligit

![Soligit Logo](public/favicon.ico)

Soligit is a powerful open-source tool designed to streamline your development workflow. It leverages AI to automatically generate comprehensive documentation for your codebases, analyze and summarize meetings, and provide intelligent insights into your projects.

## Features

- **Automated Documentation Generation:** Provide a GitHub URL and receive a full-fledged documentation website, complete with a file tree and answers to common questions about your codebase.
- **AI-Powered Q&A:** Ask questions about your codebase in natural language and get intelligent, context-aware answers.
- **Commit Summarization:** Automatically summarize the changes in a specific commit, making it easier to track project history.
- **Meeting Transcription and Analysis:** Transcribe audio meetings from a URL and use AI to summarize key points and answer questions about the discussion.
- **Secure and Scalable:** Built with a modern, robust tech stack to ensure reliability and performance.

## Tech Stack

### Frontend

- [Next.js](https://nextjs.org/)
- [React](https://reactjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [tRPC](https://trpc.io/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Clerk](https://clerk.com/) for authentication

### Backend

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Weaviate](https://weaviate.io/) for vector search
- [Google Gemini](https://gemini.google.com/) for generative AI
- [AssemblyAI](https://www.assemblyai.com/) for audio transcription

## Getting Started

### Prerequisites

- Node.js (v18 or later)
- Python (v3.9 or later)
- `pip` and `virtualenv` for Python package management
- A PostgreSQL database

### Installation

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

## Project Structure

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

## License

This project is licensed under the **Apache 2.0 License**. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## Security

For any security-related concerns, please refer to our [Security Policy](SECURITY.md).
