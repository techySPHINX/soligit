# Soligit

![Soligit Logo](public/favicon.ico)

A full-stack web application built with the T3 stack, providing a platform for users to manage their Git repositories, ask questions, and interact with a community of developers.

## Features

*   **User Authentication:** Secure user authentication with Clerk.
*   **Repository Management:** Add and manage your Git repositories.
*   **Q&A Platform:** Ask questions and get answers from the community.
*   **tRPC API:** End-to-end typesafe APIs with tRPC.
*   **Prisma ORM:** Modern database access with Prisma.
*   **Next.js:** Server-side rendering and static site generation with Next.js.
*   **Tailwind CSS:** A utility-first CSS framework for rapid UI development.

## Tech Stack

*   [Next.js](https://nextjs.org/)
*   [React](https://reactjs.org/)
*   [TypeScript](https://www.typescriptlang.org/)
*   [tRPC](https://trpc.io/)
*   [Prisma](https://www.prisma.io/)
*   [Tailwind CSS](https://tailwindcss.com/)
*   [Clerk](https://clerk.com/)

## Getting Started

### Prerequisites

*   Node.js (v18 or later)
*   npm or yarn
*   Docker (for running the database locally)

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/your-username/soligit.git
    ```

2.  Install the dependencies:

    ```bash
    npm install
    ```

3.  Set up the environment variables:

    Create a `.env` file in the root of the project and add the following environment variables:

    ```bash
    # Clerk
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
    CLERK_SECRET_KEY=

    # Database
    DATABASE_URL="postgresql://user:password@localhost:5432/soligit"
    ```

4.  Start the database:

    ```bash
    docker-compose up -d
    ```

5.  Run the database migrations:

    ```bash
    npm run db:migrate
    ```

6.  Start the development server:

    ```bash
    npm run dev
    ```

## Environment Variables

*   `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`: Your Clerk publishable key.
*   `CLERK_SECRET_KEY`: Your Clerk secret key.
*   `DATABASE_URL`: The connection string for your PostgreSQL database.

## Database

This project uses Prisma as the ORM and PostgreSQL as the database. The database schema is defined in the `prisma/schema.prisma` file.

To run the database locally, you can use the `docker-compose.yml` file provided in the root of the project.

## Available Scripts

*   `npm run dev`: Starts the development server.
*   `npm run build`: Builds the application for production.
*   `npm run start`: Starts the production server.
*   `npm run lint`: Lints the code.
*   `npm run format`: Formats the code with Prettier.
*   `npm run db:migrate`: Runs the database migrations.
*   `npm run db:studio`: Opens the Prisma Studio.

## Linting and Formatting

This project uses ESLint for linting and Prettier for formatting. You can run the linter and formatter with the following commands:

```bash
npm run lint
npm run format
```

## Deployment

To deploy the application, you can use a platform like Vercel or Netlify. You will need to set up the environment variables on the deployment platform.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.