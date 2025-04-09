"use client"
import { useBookFilters } from "@/hooks/useBookFilters";
import { BookData } from "../lib/types";
import BookCards from "../ui/book-cards";
import PageHeader from "../ui/page-header";
import SearchAndFilters from "../ui/search-and-filters";
import { useEffect } from "react";

const books: BookData[] = [

]

export default function Favorites() {
	const { displayedBooks, searchQuery, sortOption, ascending, genreFilter, softFilter,
		setSearchQuery, setSortOption, setAscending, setGenreFilter, setSoftFilter, setBooks } = useBookFilters(books)

	useEffect(() => { setBooks(books) }, [])


	return (
		<div className="flex flex-col flex-nowrap w-full pl-2.5 pr-2.5">
			<PageHeader title="My Favorite Books!" />
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