import * as React from "react"

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

export function SortSelect({ className, sortOption, setSortOption }: { className: string, sortOption: string, setSortOption: React.Dispatch<React.SetStateAction<string>> }) {
    return (
        <div className={className}>
            <Select value={sortOption} onValueChange={setSortOption}>
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
