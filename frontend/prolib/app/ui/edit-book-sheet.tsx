"use client"
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
import { ChangeEvent, Dispatch, useState } from "react"
import { BookEditable } from "../lib/types"
import { Textarea } from "@/components/ui/textarea"
import CategorySelectionBadges from "./category-selection-badges"

export function EditBookSheet({ text, book, changeEventHandler, submitHandler }: { text: string, book: BookEditable, changeEventHandler: (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void, submitHandler: () => void }) {
    const [categoriesList, setCategoriesList] = useState<{ categories: string[] }>({ categories: book.Categories });
    const [selectedCategory, setSelectedCategory] = useState("");

    console.log(book, "book")
    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button size="lg" className="w-full sm:w-auto">
                    <PenBox className="h-4 w-4 mr-2" />
                    {text}
                </Button>
            </SheetTrigger>
            <SheetContent className="overflow-y-auto">
                <SheetHeader>
                    <SheetTitle>Edit Book</SheetTitle>
                    <SheetDescription>
                        Make changes to the book here. Click save when you're done.
                    </SheetDescription>
                </SheetHeader>
                <div className="grid gap-4 py-4">
                    {Object.entries(book).map(([key, value]) => {
                        console.log(key, value, "keyval")
                        if (key == "id") return
                        if (key == "Authors") return (// field that explains to add comma for multiple authors
                            <div className="grid grid-cols-4 items-center gap-4 gap-y-1" key={key}>
                                <Label htmlFor={key} className="block text-right">
                                    {key}
                                </Label>
                                <Input id={key} value={value} onChange={(e) => changeEventHandler(e)} className="w-[90%] col-span-3" />
                                <p className="text-sm text-gray-500 col-span-4 ml-5 mr-5" key={`${key}P`} >Separate multiple authors with commas (e.g., "J.K. Rowling, John Smith")</p>
                            </div>
                        )
                        if (key == "Description") return (// Return a textarea instead of an input field
                            <div className="grid grid-cols-4 items-start gap-4" key={key}>
                                <Label htmlFor={key} className="block text-right">
                                    {key}
                                </Label>
                                <Textarea
                                    id={key}
                                    name={key}
                                    key={`${key}TextArea`}
                                    placeholder="Enter book description"
                                    value={value as string}
                                    onChange={(e) => changeEventHandler(e)}
                                    className="min-h-32 w-[90%] col-span-3"
                                />
                            </div>
                        )
                        if (key == "Categories") return <CategorySelectionBadges classNames="grid grid-cols4 items-center gap-1 ml-3 mr-3" key={"categorySelectionBadges"} formData={categoriesList} setFormData={setCategoriesList}
                            selectedCategory={selectedCategory} setSelectedCategory={setSelectedCategory} />

                        // if (value == undefined) return

                        return <div className="grid grid-cols-4 items-center gap-4" key={key}>
                            <Label htmlFor="title" className="block text-right">
                                {key}
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
