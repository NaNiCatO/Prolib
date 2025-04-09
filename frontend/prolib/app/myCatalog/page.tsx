"use client"
import { useEffect, useState } from "react";
import { BookData, BookDataAPI } from "../lib/types";
import BookCards from "../ui/book-cards";
import PageHeader from "../ui/page-header";
import SearchAndFilters from "../ui/search-and-filters";
import { useBookFilters } from "@/hooks/useBookFilters";
import { findCustomBooks, makeBookDataFromAPI } from "../lib/bookDataFormatting";

const booksHardCoded: BookData[] = [
    {
        id: "5", isCustomBook: true, isFavorite: true, description: "No description", language: "English", pageCount: "13", publisher: "Nino", publishedDate: "Today",
        title: "My Diary", authors: ["Nino"], coverUrl: "/diary.jpg", categories: ["non-fiction"], rating: null, ratingCount: null
    },
    {
        id: "6", isCustomBook: true, isFavorite: true, description: "No description", language: "English", pageCount: "13", publisher: "Nino", publishedDate: "Today",
        title: "Next.js", authors: ["Nino"], coverUrl: "/nextjs.jpg", categories: ["non-fiction"], rating: null, ratingCount: null
    }
]

export default function MyCatalog() {
    const [books, setBooks] = useState<BookData[]>(booksHardCoded)

    const { displayedBooks, searchQuery, sortOption, ascending, genreFilter, softFilter,
        setSearchQuery, setSortOption, setAscending, setGenreFilter, setSoftFilter } = useBookFilters(books)

    // Fetch books initial
    useEffect(() => {
        async function fetchBooks() {
            try {
                const response = await fetch(new URL('http://localhost:8000/books'));
                console.log(response, "response")
                const data: BookDataAPI[] = await response.json();
                console.log(data, "data")
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