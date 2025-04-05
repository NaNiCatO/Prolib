import * as React from "react"

import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

export function FilterSelect({ className }: { className: string }) {
    return (
        <div className={className}>
            <Select>
                <SelectTrigger className="w-full">
                    <SelectValue placeholder="Sort By" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="title">Title</SelectItem>
                    <SelectItem value="author">Author</SelectItem>
                    <SelectItem value="rating">Rating</SelectItem>
                </SelectContent>
            </Select>
        </div>
    )
}
