"use client"
import PageHeader from "../ui/page-header";
import SearchAndFilters from "../ui/search-and-filters";
import { BookData } from "../lib/types";
import BookCards from "../ui/book-cards";
import { useBookFilters } from "@/hooks/useBookFilters";
import { useEffect } from "react";

const books: BookData[] = [
  { id: "0", title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: ["adventure", "fantasy"], rating: 2.5, ratingCount: 17 },
  { id: "1", title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: ["horror", "mystery"], rating: 3.5, ratingCount: 11 },
  { id: "2", title: "My Little Pony", author: "G. M. Berrow", cover: "/mlp.jpg", genre: ["horror"], rating: 0.5, ratingCount: 127 },
  { id: "3", title: "Spongebob", author: "Stephen Hillenburg", cover: "/spongebob.jpg", genre: ["mystery"], rating: 0, ratingCount: 29 },
  { id: "4", title: "Tom & Jerry", author: "William Hanna", cover: "/tomandjerry.jpg", genre: ["art"], rating: 5, ratingCount: 16 },
  // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 4.5, ratingCount: 17 },
  // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
  // { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", genre: "fiction", rating: 3.5, ratingCount: 17 },
];

export default function Library() {
  const { displayedBooks, searchQuery, sortOption, ascending, genreFilter, softFilter,
    setSearchQuery, setSortOption, setAscending, setGenreFilter, setSoftFilter, setBooks } = useBookFilters(books)

  // // Fetch books
  // useEffect(() => {
  //   async function fetchBooks() {
  //     try {
  //       const response = await fetch('/api/books');
  //       const data = await response.json();
  //       setBooks(data);
  //     } catch (error) {
  //       console.error('Error fetching books:', error);
  //     }
  //   }

  //   fetchBooks();
  // }, [setBooks]);

  useEffect(() => { setBooks(books) }, [])
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
