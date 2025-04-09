import { generateUUID } from "@/lib/utils";
import { AddBookData, BookData, BookDataAPI, BookEditable } from "./types";

export const makeBookDataFromAPI = (bookDataAPI: BookDataAPI[]): BookData[] => {
    const bookData: BookData[] = bookDataAPI.map(b => ({
        id: b.id,
        isCustomBook: b.data.isCustomBook,
        isFavorite: b.data.isFavorite,
        title: b.data.Title,
        authors: b.data.Authors,
        publisher: b.data.Publisher,
        publishedDate: b.data.PublishedDate,
        description: b.data.Description,
        isbn10: b.data.ISBN10,
        isbn13: b.data.ISBN13,
        pageCount: b.data.PageCount.toString(),
        categories: b.data.Categories,
        language: b.data.Language,
        coverUrl: b.data.Thumbnail,
        rating: b.data.AvgRating,
        ratingCount: b.data.PeopleRated
    }))

    return bookData
}

export const updateBookDataFromEditable = (bookData: BookData, bookDataEditable: BookEditable): BookData => {
    const b = bookData
    const be = bookDataEditable
    const newBookData: BookData = { ...b, ...be }

    return newBookData
}

export const makeBookEditable = (book: BookData): BookEditable => {
    const bookEditable: BookEditable = {
        id: book.id,
        title: book.title,
        authors: book.authors,
        publisher: book.publisher,
        publishedDate: book.publishedDate,
        description: book.description,
        pageCount: book.pageCount,
        categories: book.categories,
        language: book.language,
        coverUrl: book.coverUrl
    }

    return bookEditable
}

export const makeAPIFromBookData = (book: BookData): BookDataAPI => {
    const bookDataApi: BookDataAPI = {
        id: book.id,
        data: {
            isCustomBook: book.isCustomBook,
            isFavorite: book.isFavorite,
            Title: book.title,
            Authors: book.authors,
            Publisher: book.publisher,
            PublishedDate: book.publishedDate,
            Description: book.description,
            ISBN10: book.isbn10 ?? "",
            ISBN13: book.isbn13 ?? "",
            PageCount: parseInt(book.pageCount),
            Categories: book.categories,
            Language: book.language,
            Thumbnail: book.coverUrl,
            AvgRating: book.rating,
            PeopleRated: book.ratingCount
        }
    }

    return bookDataApi
}

export const makeAPIFromAddBookData = (book: AddBookData): BookDataAPI => {
    const bookDataApi: BookDataAPI = {
        id: "",
        data: {
            isCustomBook: true,
            isFavorite: false,
            Title: book.title,
            Authors: book.authors,
            Publisher: book.publisher,
            PublishedDate: book.publishedDate,
            Description: book.description,
            ISBN10: "",
            ISBN13: "",
            PageCount: parseInt(book.pageCount),
            Categories: book.categories,
            Language: book.language,
            Thumbnail: book.coverUrl,
            AvgRating: null,
            PeopleRated: null
        }
    }

    return bookDataApi
}

export const findCustomBooks = (allBooks: BookDataAPI[]) => {
    return allBooks.filter(b => b.data.isCustomBook)
}

export const findFavoriteBooks = (allBooks: BookDataAPI[]) => {
    return allBooks.filter(b => b.data.isFavorite)
}