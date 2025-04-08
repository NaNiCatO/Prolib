"use client"
import { useEffect } from "react";
import { BookData } from "../lib/types";
import BookCards from "../ui/book-cards";
import PageHeader from "../ui/page-header";
import SearchAndFilters from "../ui/search-and-filters";
import { useBookFilters } from "@/hooks/useBookFilters";

const books: BookData[] = [
    { id: "5", title: "My Diary", author: "Nino", cover: "/diary.jpg", genre: ["non-fiction"], rating: null, ratingCount: null },
    { id: "6", title: "Next.js", author: "Nino", cover: "/nextjs.jpg", genre: ["non-fiction"], rating: null, ratingCount: null }
]

export default function MyCatalog() {
    const { displayedBooks, searchQuery, sortOption, ascending, genreFilter, softFilter,
        setSearchQuery, setSortOption, setAscending, setGenreFilter, setSoftFilter, setBooks } = useBookFilters(books)

    useEffect(() => { setBooks(books) }, [])

    return (
        <div className="flex flex-col flex-nowrap w-full pl-2.5 pr-2.5">
            <PageHeader title="My Catalog" />
            <SearchAndFilters
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                sortOption={sortOption}
                setSortOption={setSortOption}
                ascending={ascending}
                setAscending={setAscending}
                genreFilter={genreFilter}
                setGenreFilter={setGenreFilter}
                softFilter={softFilter}
                setSoftFilter={setSoftFilter}
            />
            <BookCards books={displayedBooks} />
        </div>
    );
}