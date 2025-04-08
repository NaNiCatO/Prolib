"use client"
import { BookData } from '@/app/lib/types';
import { useState, useEffect } from 'react';

export function useBookFilters(initialBooks: BookData[] = []) {
    const [books, setBooks] = useState(initialBooks);
    const [displayedBooks, setDisplayedBooks] = useState(initialBooks);
    const [searchQuery, setSearchQuery] = useState('');
    const [sortOption, setSortOption] = useState('title');
    const [ascending, setAscending] = useState(true);
    const [genreFilter, setGenreFilter] = useState<string[]>([]);
    const [softFilter, setSoftFilter] = useState(false)

    // Update books if initialBooks changes (e.g., from API)
    useEffect(() => {
        setBooks(initialBooks);
    }, [initialBooks]);

    // Apply filters whenever filter states or books change
    useEffect(() => {
        let filteredBooks = [...books];

        // Apply search
        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            filteredBooks = filteredBooks.filter(book =>
                book.title.toLowerCase().includes(query) ||
                book.author.toLowerCase().includes(query)
            );
        }

        // Apply genre filter
        if (genreFilter.length > 0) {
            if (softFilter) filteredBooks = filteredBooks.filter(book => book.genre.some(g => genreFilter.includes(g)))
            else filteredBooks = filteredBooks.filter(book => genreFilter.every(g => book.genre.includes(g)));
        }

        // Apply sorting
        switch (sortOption) {
            case 'title':
                filteredBooks.sort((a, b) => a.title.localeCompare(b.title));
                break;
            case 'author':
                filteredBooks.sort((a, b) => a.author.localeCompare(b.author));
                break;
            case 'rating':
                filteredBooks.sort((a, b) => {
                    a.rating = a.rating ?? -1
                    b.rating = b.rating ?? -1
                    return a.rating - b.rating
                });
                break;
            default:
                break;
        }
        if (!ascending) filteredBooks.reverse()

        setDisplayedBooks(filteredBooks);
    }, [searchQuery, sortOption, ascending, genreFilter, softFilter, books]);

    // Expose filter controls and results
    return {
        // Results
        displayedBooks,

        // Filter states
        searchQuery,
        sortOption,
        ascending,
        genreFilter,
        softFilter,

        // Filter setters
        setSearchQuery,
        setSortOption,
        setAscending,
        setGenreFilter,
        setSoftFilter,

        // Books setter (for updating from API)
        setBooks
    };
}