"use client"
import PageHeader from "../ui/page-header";
import SearchAndFilters from "../ui/search-and-filters";
import { BookData, BookDataAPI } from "../lib/types";
import BookCards from "../ui/book-cards";
import { useBookFilters } from "@/hooks/useBookFilters";
import { useEffect, useState } from "react";
import { makeBookDataFromAPI } from "../lib/bookDataFormatting";

// const books: BookData[] = [
//     {
//         id: "0", isCustomBook: false, isFavorite: false, description: "No description", isbn10: "", isbn13: "7812372981392132", language: "English",
//         pageCount: "32", publishedDate: "IDK", publisher: "IDK", title: "Garfield", authors: ["Jim Davis"], coverUrl: "/garfield.jpg", categories: ["adventure", "fantasy"],
//         rating: 2.5, ratingCount: 17
//     },
//     {
//         id: "1", isCustomBook: false, isFavorite: false, description: "No description", isbn10: "", isbn13: "7812372981392132", language: "English",
//         pageCount: "32", publishedDate: "IDK", publisher: "IDK", title: "Oggy", authors: ["Jordan Gershowitz"], coverUrl: "/oggy.jpg", categories: ["horror", "mystery"],
//         rating: 3.5, ratingCount: 11
//     },
//     {
//         id: "2", isCustomBook: false, isFavorite: false, description: "No description", isbn10: "", isbn13: "7812372981392132", language: "English",
//         pageCount: "32", publishedDate: "IDK", publisher: "IDK", title: "My Little Pony", authors: ["G. M. Berrow"], coverUrl: "/mlp.jpg", categories: ["horror"],
//         rating: 0.5, ratingCount: 127
//     },
//     {
//         id: "3", isCustomBook: false, isFavorite: false, description: "No description", isbn10: "", isbn13: "7812372981392132", language: "English",
//         pageCount: "32", publishedDate: "IDK", publisher: "IDK", title: "Spongebob", authors: ["Stephen Hillenburg"], coverUrl: "/spongebob.jpg", categories: ["mystery"],
//         rating: 0, ratingCount: 29
//     },
//     {
//         id: "4", isCustomBook: false, isFavorite: false, description: "No description", isbn10: "", isbn13: "7812372981392132", language: "English",
//         pageCount: "32", publishedDate: "IDK", publisher: "IDK", title: "Tom & Jerry", authors: ["William Hanna"], coverUrl: "/tomandjerry.jpg", categories: ["art"],
//         rating: 5, ratingCount: 16
//     },
//     // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 4.5, ratingCount: 17 },
//     // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
//     // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
// ];

export default function Library() {
    const [books, setBooks] = useState<BookData[]>([])

    let { displayedBooks, searchQuery, sortOption, ascending, genreFilter, softFilter,
        setSearchQuery, setSortOption, setAscending, setGenreFilter, setSoftFilter } = useBookFilters(books)

    // Fetch books initial
    useEffect(() => {
        async function fetchBooks() {
            try {
                const response = await fetch(new URL('http://localhost:8000/books'));
                console.log(response, "response")
                const data: BookDataAPI[] = await response.json();
                console.log(data, "data")
                const formattedData = makeBookDataFromAPI(data)
                setBooks(formattedData);
            } catch (error) {
                console.error('Error fetching books:', error);
            }
        }

        fetchBooks();
    }, []);

    // useEffect(() => {
    //     async function fetchBooks() {
    //         try {
    //             const response = await fetch('/api/books');
    //             const data = await response.json();
    //             setBooks(data);
    //         } catch (error) {
    //             console.error('Error fetching books:', error);
    //         }
    //     }

    //     fetchBooks();
    // }, [setBooks]);

    // useEffect(() => { setBooks(books) }, [])
    // console.log(books, "total books")
    // console.log(displayedBooks, "displayed books")

    // setBooks(books)

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
            <BookCards books={displayedBooks} />
        </div>
    );
}
