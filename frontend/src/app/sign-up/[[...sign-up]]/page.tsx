import { SignUp } from "@clerk/nextjs";
import { BackgroundBeams } from "../../../components/ui/background-beams";

export default function Page() {
  return (
    <div className="h-screen w-full rounded-md bg-neutral-950 relative flex flex-col items-center justify-center antialiased">
      <div className="max-w-2xl mx-auto p-4">
        <SignUp />
      </div>
      <BackgroundBeams />
    </div>
  );
}
