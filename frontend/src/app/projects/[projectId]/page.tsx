import AddRepo from "../../../components/AddRepo";
import CommitLog from "../../../components/CommitLog";
import { db } from "../../../server/db";
import {
  BookText,
  ExternalLink,
  FileQuestion,
  Github,
  Presentation,
} from "lucide-react";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import React from "react";
import { Button } from "../../../components/ui/button";
import InviteButton from "../../../components/InviteButton";
import { auth } from "@clerk/nextjs/server";
import TeamMembers from "../../../components/TeamMembers";
import { HoverEffect } from "../../../components/ui/card-hover-effect";

type Props = {
  params: {
    projectId: string;
  };
};

const ProjectID = async ({ params: { projectId } }: Props) => {
  const { userId } = await auth();
  const user = await db.user.findUnique({
    where: {
      id: userId ?? "",
    },
  });
  if (!user) {
    return redirect("/register-user");
  }

  const project = await db.project.findUnique({
    where: { id: projectId },
    include: {
      commits: {
        orderBy: {
          commitDate: "desc",
        },
      },
      users: true,
    },
  });
  if (!project) {
    return notFound();
  }

  const projectCards = [
    {
      title: "Ask a Question",
      description: "Get answers to your questions about the project.",
      link: `/qna/${project.id}`,
    },
    {
      title: "Meetings",
      description: "View and schedule meetings for the project.",
      link: `/meetings/${project.id}`,
    },
    {
      title: "Documentation",
      description: "Read the project documentation.",
      link: `/documentation/${project.id}`,
    },
  ];

  return (
    <>
      {!project.githubUrl && (
        <div className="flex items-center justify-center">
          <AddRepo projectId={project.id} />
        </div>
      )}
      {project.githubUrl && (
        <>
          <div className="flex items-center justify-between">
            <div className="w-fit rounded-md bg-gray-900 px-4 py-3">
              <div className="flex items-center">
                <Github className="h-5 w-5 text-white" />
                <div className="ml-2">
                  <p className="text-sm font-medium text-white">
                    This project is linked to{" "}
                    <Link
                      className="inline-flex items-center text-gray-300 hover:underline"
                      href={project.githubUrl}
                    >
                      {project.githubUrl}
                      <ExternalLink className="ml-1 h-4 w-4" />
                    </Link>
                  </p>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Link href={`/documentation/${project.id}`}>
                <Button size="icon">
                  <BookText />
                </Button>
              </Link>
              <Link href={`/qna/${project.id}`}>
                <Button size="icon">
                  <FileQuestion />
                </Button>
              </Link>
              <Link href={`/meetings/${project.id}`}>
                <Button size="icon">
                  <Presentation />
                </Button>
              </Link>
            </div>
          </div>
          <div className="mt-4 flex items-center">
            <InviteButton projectId={project.id} />
            <div className="w-4"></div>
            <TeamMembers projectId={project.id} users={project.users} />
          </div>
          <div className="mt-4">
            <HoverEffect items={projectCards} />
          </div>
          <div className="mt-8">
            <CommitLog project={project} />
          </div>
        </>
      )}
    </>
  );
};

export default ProjectID;