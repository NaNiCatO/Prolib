"use client"
import PageHeader from "../ui/page-header";
import SearchAndFilters from "../ui/search-and-filters";
import { BookData, BookDataAPI } from "../lib/types";
import BookCards from "../ui/book-cards";
import { useBookFilters } from "@/hooks/useBookFilters";
import { useEffect, useState } from "react";
import { makeBookDataFromAPI } from "../lib/bookDataFormatting";
import { BookCardSkeleton } from "../ui/book-cards-skeleton";

export default function Library() {
    const [books, setBooks] = useState<BookData[]>([])
    const [isLoading, setIsLoading] = useState(true)

    let { displayedBooks, searchQuery, sortOption, ascending, genreFilter, softFilter,
        setSearchQuery, setSortOption, setAscending, setGenreFilter, setSoftFilter } = useBookFilters(books)

    // Fetch books initial
    useEffect(() => {
        async function fetchBooks() {
            try {
                setIsLoading(true);
                const response = await fetch(new URL('http://localhost:8000/books'));
                const data: BookDataAPI[] = await response.json();
                const formattedData = makeBookDataFromAPI(data)
                setBooks(formattedData);
            } catch (error) {
                console.error('Error fetching books:', error);
            } finally {
                setIsLoading(false);
            }
        }

        fetchBooks();
    }, []);

    return (
        <div className="flex flex-col flex-nowrap w-full pl-2.5 pr-2.5">
            <PageHeader title="Find a book to read!" />
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
            {isLoading ? (
                <div className="flex flex-wrap gap-4 mt-6">
                    <BookCardSkeleton count={20} />
                </div>
            ) : (
                <BookCards books={displayedBooks} />
            )}
        </div>
    );
}
