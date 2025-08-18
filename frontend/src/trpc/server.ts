import {
  createTRPCProxyClient,
  httpBatchLink,
} from "@trpc/client";
import { headers } from "next/headers";

import { type AppRouter } from "../server/api/root";
import { getUrl, transformer } from "./shared";

export const api = createTRPCProxyClient<AppRouter>({
  links: [
    httpBatchLink({
      url: getUrl(),
      transformer,
       async headers() {
        const incomingHeaders = headers();
        const heads: Record<string, string> = {};
        (await incomingHeaders).forEach((value: string, key: string | number) => {
          heads[key] = value;
        });
        heads["x-trpc-source"] = "rsc";
        return heads;
      },
    }),
  ],
});
