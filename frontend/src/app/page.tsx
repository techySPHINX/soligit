import CreateProject from "../components/CreateProject";
import { db } from "../server/db";
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { TextGenerateEffect } from "@/components/ui/text-generate-effect";

export default async function Index() {
  const { userId } = await auth();
  const user = await db.user.findUnique({
    where: {
      id: userId ?? "",
    },
  });
  if (!user) {
    return redirect("/register-user");
  }
  const projects = await db.project.findMany({
    where: {
      users: {
        some: {
          id: user.id,
        },
      },
    },
  });
  if (projects.length === 0) {
    return (
      <div className="container mx-auto h-full flex flex-col items-center justify-center">
        <TextGenerateEffect words="Begin by creating a new project!" />
        <CreateProject />
      </div>
    );
  } else {
    return redirect("/projects/" + projects[0]!.id);
  }
}