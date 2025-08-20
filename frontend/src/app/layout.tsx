import "../styles/globals.css";
import { headers } from "next/headers";
import { ClerkProvider } from "@clerk/nextjs";
import { TRPCReactProvider } from "../trpc/react";
import { Toaster } from "sonner";
import ApplicationShell from "../components/ApplicationShell";
import ErrorBoundary from "../components/ErrorBoundary";

export const metadata = {
  title: "Soligit",
  icons: [{ rel: "icon", url: "/favicon.ico" }],
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const headersList = await headers();
  return (
    <ClerkProvider>
      <html lang="en" className="h-full bg-white">
        <body
          className={`font-sans grainy min-h-screen`}
        >
          <TRPCReactProvider headers={headersList}>
            <ErrorBoundary>
              <ApplicationShell>{children}</ApplicationShell>
            </ErrorBoundary>
          </TRPCReactProvider>
          <Toaster richColors />
        </body>
      </html>
    </ClerkProvider>
  );
}
