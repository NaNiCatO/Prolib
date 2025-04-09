"use client"
import { useEffect, useState } from "react";
import { BookData, BookDataAPI } from "../lib/types";
import BookCards from "../ui/book-cards";
import PageHeader from "../ui/page-header";
import SearchAndFilters from "../ui/search-and-filters";
import { useBookFilters } from "@/hooks/useBookFilters";
import { findCustomBooks, makeBookDataFromAPI } from "../lib/bookDataFormatting";

export default function MyCatalog() {
    const [books, setBooks] = useState<BookData[]>([])

    const { displayedBooks, searchQuery, sortOption, ascending, genreFilter, softFilter,
        setSearchQuery, setSortOption, setAscending, setGenreFilter, setSoftFilter } = useBookFilters(books)

    // Fetch books initial
    useEffect(() => {
        async function fetchBooks() {
            try {
                const response = await fetch(new URL('http://localhost:8000/books'));
                const data: BookDataAPI[] = await response.json();
                const formattedData = makeBookDataFromAPI(findCustomBooks(data))
                setBooks(formattedData);
            } catch (error) {
                console.error('Error fetching books:', error);
            }
        }

        fetchBooks();
    }, []);

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