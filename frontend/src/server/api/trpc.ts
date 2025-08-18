/**
 * YOU PROBABLY DON'T NEED TO EDIT THIS FILE, UNLESS:
 * 1. You want to modify request context (see Part 1).
 * 2. You want to create a new middleware or type of procedure (see Part 3).
 *
 * TL;DR - This is where all the tRPC server stuff is created and plugged in. The pieces you will
 * need to use are documented accordingly near the end.
 */

import { initTRPC } from "@trpc/server";
import { type CreateNextContextOptions } from "@trpc/server/adapters/next";
import superjson from "superjson";
import { ZodError } from "zod";
import * as trpc from "@trpc/server";
import { getAuth } from "@clerk/nextjs/server";
import { db } from "../db";

/**
 * 1. CONTEXT
 *
 * Defines the "contexts" available in the backend API.
 */

export const createContextInner = ({ userId }: { userId: string | null }) => {
  return {
    auth: { userId },
    db,
  };
};

/**
 * Actual context used in router. Processes every request.
 */

export const createTRPCContext = (opts: CreateNextContextOptions) => {
  const { userId } = getAuth(opts.req);
  return createContextInner({ userId });
};

export type Context = trpc.inferAsyncReturnType<typeof createTRPCContext>;

/**
 * 2. INITIALIZATION
 */

const t = initTRPC.context<Context>().create({
  transformer: superjson,
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    };
  },
});

/**
 * 3. ROUTER & PROCEDURE
 */

export const createTRPCRouter = t.router;

/**
 * Middleware to ensure user is authenticated and inject full user object
 */

const isAuthed = t.middleware(async ({ ctx, next }) => {
  if (!ctx.auth.userId) {
    throw new trpc.TRPCError({ code: "UNAUTHORIZED" });
  }

  const user = await db.user.findUnique({
    where: { id: ctx.auth.userId },
  });

  if (!user) {
    throw new trpc.TRPCError({ code: "UNAUTHORIZED" });
  }

  return next({
    ctx: {
      ...ctx,
      user, 
    },
  });
});

/**
 * Public (unauthenticated) procedure
 */

export const publicProcedure = t.procedure;

/**
 * Protected (authenticated) procedure
 */

export const protectedProcedure = t.procedure.use(isAuthed);
