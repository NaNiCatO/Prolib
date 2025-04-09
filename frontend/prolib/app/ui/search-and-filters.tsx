"use client"
import { Input } from "@/components/ui/input";
import { ArrowDownAZ, ArrowUpZA, Filter, Search } from "lucide-react";
import { SortSelect } from "./book-sort-select";
import { Button } from "@/components/ui/button";
import { Dispatch, SetStateAction, useState } from "react";
import { Dialog, DialogClose, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import GENRES from "../lib/bookGenres.json"
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

export default function SearchAndFilters({ searchQuery, setSearchQuery, sortOption, setSortOption,
    ascending, setAscending, genreFilter, setGenreFilter, softFilter, setSoftFilter }:
    {
        searchQuery: string; setSearchQuery: Dispatch<SetStateAction<string>>
        sortOption: string; setSortOption: Dispatch<SetStateAction<string>>
        ascending: boolean; setAscending: Dispatch<SetStateAction<boolean>>
        genreFilter: string[]; setGenreFilter: Dispatch<SetStateAction<string[]>>
        softFilter: boolean; setSoftFilter: Dispatch<SetStateAction<boolean>>
    }
) {
    const [selectedGenreFilters, setSelectedGenreFilters] = useState(genreFilter)
    const [selectedSoftFilter, setSelectedSoftFilter] = useState(softFilter)

    const toggleAscending = () => setAscending(bool => !bool);

    return (
        <div className="m-7 flex flex-nowrap justify-between items-center">
            <div className="relative basis-2/3 w-full">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={17} />
                <Input
                    type="text"
                    placeholder="Search books..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full min-w-xs rounded-lg pl-10"
                />
            </div>
            <div className="flex justify-between basis-1/3 ml-2">
                {/* <Button variant="outline" className="grow m-1">
            Cover <ChevronDown size={16} />
          </Button> */}
                {/* <Button variant="outline" className="grow m-1">
            Title <ChevronDown size={16} />
          </Button> */}
                <SortSelect className="grow m-1" sortOption={sortOption} setSortOption={setSortOption} />
                <Button variant="outline" className="m-1" size={"icon"} onClick={toggleAscending}>
                    {ascending ? <ArrowDownAZ /> : <ArrowUpZA />}
                </Button>
                <Dialog onOpenChange={open => {
                    if (!open) {
                        setSelectedGenreFilters(genreFilter)
                        setSelectedSoftFilter(softFilter)
                    }
                }}>
                    <DialogTrigger asChild>
                        <Button variant="default" className="grow m-1">
                            <Filter size={16} className="mr-2" /> Filter
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="w-auto">
                        <DialogHeader>
                            <DialogTitle>Select Genres to filter</DialogTitle>
                            <DialogDescription>You may select more than one.</DialogDescription>
                        </DialogHeader>
                        <div className="flex flex-wrap">
                            {GENRES.map(genre =>
                                <div className="flex m-2" key={`${genre.value}Div`}>
                                    <Checkbox
                                        id={`${genre.value}Checkbox`}
                                        key={`${genre.value}Checkbox`}
                                        defaultChecked={genreFilter.includes(genre.name)}
                                        checked={selectedGenreFilters.includes(genre.name)}
                                        onCheckedChange={(isChecked) => setSelectedGenreFilters(selectedGenres => {
                                            if (isChecked && !selectedGenreFilters.includes(genre.name)) return [...selectedGenres, genre.name]
                                            else if (!isChecked && selectedGenreFilters.includes(genre.name)) return selectedGenres.filter(g => g != genre.name)
                                            else return selectedGenres
                                        })}
                                    />
                                    <Label htmlFor={`${genre.value}Checkbox`} className="ml-1">{genre.name}</Label>
                                </div>
                            )}
                        </div>
                        <DialogFooter>
                            <Checkbox
                                id="softFilterCheckbox"
                                key="softFilterCheckbox"
                                defaultChecked={softFilter}
                                checked={selectedSoftFilter}
                                onCheckedChange={isChecked => setSelectedSoftFilter(!!isChecked)}
                            />
                            <div className="grid gap-1.5 leading-none mr-5">
                                <Label htmlFor="softFilterCheckbox" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">Soft Filter</Label>
                                <p className="text-sm text-muted-foreground">Will match any book that has at least 1 selected genre.</p>
                            </div>
                            <Button variant={"secondary"} onClick={() => { setSelectedGenreFilters([]); setSelectedSoftFilter(false) }} >Clear Filters</Button>
                            <DialogClose asChild>
                                <Button variant="default" onClick={() => { setGenreFilter(selectedGenreFilters); setSoftFilter(selectedSoftFilter) }}>
                                    <Filter size={16} className="mr-2" /> Filter
                                </Button>
                            </DialogClose>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>
        </div>
    )
}