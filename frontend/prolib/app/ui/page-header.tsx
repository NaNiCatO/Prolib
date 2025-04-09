import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { CircleUser } from "lucide-react";

export default function PageHeader({ title }: { title: string }) {
    return (
        <header className="flex h-12 shrink-0 justify-between justify-items-center items-center gap-2 border-b-2 transition-[width,height] ease-linear">
            <h1 className="m-5 text-4xl">{title}</h1>

            <Avatar className="w-13 h-13 mb-2 mr-6">
                <AvatarImage />
                <AvatarFallback><CircleUser size={50} /></AvatarFallback>
            </Avatar>
        </header>
    )
}