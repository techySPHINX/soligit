import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { type NextRequest } from "next/server";

import { env } from "~/env";
import { appRouter } from "~/server/api/root";
import { createContextInner } from "~/server/api/trpc";
import { getAuth } from "@clerk/nextjs/server";

/**
 * Custom context function compatible with NextRequest (App Router).
 */
const createContext =  (req: NextRequest) => {
  const auth = getAuth(req);
  return createContextInner({ userId: auth.userId });
};

const handler = (req: NextRequest) =>
  fetchRequestHandler({
    endpoint: "/api/trpc",
    req,
    router: appRouter,
    createContext: () => createContext(req),
    onError:
      env.NODE_ENV === "development"
        ? ({ path, error }) => {
            console.error(`❌ tRPC failed on ${path ?? "<no-path>"}: ${error.message}`);
          }
        : undefined,
  });

export { handler as GET, handler as POST };
