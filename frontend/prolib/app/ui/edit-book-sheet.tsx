import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
    Sheet,
    SheetClose,
    SheetContent,
    SheetDescription,
    SheetFooter,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from "@/components/ui/sheet"
import { PenBox } from "lucide-react"
import { ChangeEvent, Dispatch } from "react"
import { BookEditable } from "../lib/types"
import { camelCaseToWords } from "@/lib/utils"

export function EditBookSheet({ text, book, changeEventHandler, submitHandler }: { text: string, book: BookEditable, changeEventHandler: (e: ChangeEvent<HTMLInputElement>) => void, submitHandler: () => void }) {
    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button size="lg" className="w-full sm:w-auto">
                    <PenBox className="h-4 w-4 mr-2" />
                    {text}
                </Button>
            </SheetTrigger>
            <SheetContent>
                <SheetHeader>
                    <SheetTitle>Edit Book</SheetTitle>
                    <SheetDescription>
                        Make changes to the book here. Click save when you're done.
                    </SheetDescription>
                </SheetHeader>
                <div className="grid gap-4 py-4">
                    {Object.entries(book).map(([key, value], index) => {
                        if (key == "id") return
                        if (key == "authors") return // field that explains to add comma for multiple authors
                        if (key == "description") return // Return a textarea instead of an input field
                        if (key == "categories") return // Multiple Genre selections

                        return <div className="grid grid-cols-4 items-center gap-4" key={index}>
                            <Label htmlFor="title" className="block text-right">
                                {camelCaseToWords(key)}
                            </Label>
                            <Input id={key} value={value} onChange={(e) => changeEventHandler(e)} className="w-[90%] col-span-3" />
                        </div>
                    })}
                    {/* <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="title" className="block text-right">
                            Title
                        </Label>
                        <Input id="title" value={book.title} onChange={(e) => changeEventHandler(e)} className="w-[90%] col-span-3" />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="authors" className="block text-right">
                            Authors
                        </Label>
                        <Input id="authors" value={book.authors[0]} onChange={(e) => changeEventHandler(e)} className="w-[90%] col-span-3" />
                    </div> */}
                </div>
                <SheetFooter>
                    <SheetClose asChild>
                        <Button type="submit" onClick={() => submitHandler()}>Save changes</Button>
                    </SheetClose>
                </SheetFooter>
            </SheetContent>
        </Sheet>
    )
}
