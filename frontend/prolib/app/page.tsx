import { BookText } from "lucide-react";

export default function Home() {
  return (
    <div className="flex justify-center items-center h-screen overflow-hidden">
      <BookText style={{ width: "100px", height: "100px" }} strokeWidth={2.5} />
      <span className="text-3xl">ProLib</span>
    </div>
  );
}
