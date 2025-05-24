import {Button, buttonVariants} from "@/components/ui/button";
export default function Home() {
  return (
      <div className="flex flex-col self-center border justify-items-center">
        Test!!!
        <Button className={buttonVariants({variant: "default"})}>Click Me</Button>
      </div>
      );
}
